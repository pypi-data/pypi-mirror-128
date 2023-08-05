"""An implementation of the Corral algorithm."""

import math

from typing import Any, Sequence, Optional, Dict, Tuple

from coba.random import CobaRandom
from coba.environments import Context, Action
from coba.learners.core import Learner, SafeLearner, Probs, Info

class CorralLearner(Learner):
    """This is an implementation of the Agarwal et al. (2017) Corral algorithm.

    This algorithm assumes that the reward distribution has support in [0,1]
    and improves on the remark on pg. 8 to base learner selection efficiency.

    References:
        Agarwal, Alekh, Haipeng Luo, Behnam Neyshabur, and Robert E. Schapire. 
        "Corralling a band of bandit algorithms." In Conference on Learning 
        Theory, pp. 12-38. PMLR, 2017.
    """

    def __init__(self, base_learners: Sequence[Learner], eta: float, T: float = math.inf, type:str="importance", seed: int = 1) -> None:
        """Instantiate a CorralLearner.

        Args:
            base_learners: The collection of algorithms to use as base learners.
            eta: The learning rate. This controls how quickly Corral picks a best base_learner. 
            T: The number of interactions expected during the learning process. A small T will cause
                the learning rate to shrink towards 0 quickly while a large value for T will cause the
                learning rate to shrink towards 0 slowly. A value of inf means that the learning rate
                will remain constant.
            type: Determines the method with which feedback is provided to the base learners. The 
                original paper used importance sampling. We also support `off-policy` and `rejection`.
            seed: A seed for a random number generation in ordre to get repeatable results.
        """

        assert type in ["importance", "off-policy", "rejection"], "The provided `type` for CorralLearner was unrecognized."

        self._base_learners = [ SafeLearner(learner) for learner in base_learners]

        M = len(self._base_learners)

        self._T     = T
        self._gamma = 1/T
        self._beta  = 1/math.exp(1/math.log(T))

        self._eta_init = eta
        self._etas     = [ eta ] * M
        self._rhos     = [ float(2*M) ] * M
        self._ps       = [ 1/M ] * M
        self._p_bars   = [ 1/M ] * M

        self._type = type

        self._random_pick   = CobaRandom(seed)
        self._random_reject = CobaRandom(CobaRandom(seed).randint(0,10000))

    @property
    def params(self) -> Dict[str, Any]:
        """The parameters of the learner.

        See the base class for more information
        """
        return { "family": "corral", "eta": self._eta_init, "type":self._type, "T": self._T, "B": [ b.params["family"] for b in self._base_learners ], "seed":self._random_pick._seed }

    def predict(self, context: Context, actions: Sequence[Action]) -> Tuple[Probs, Info]:
        """Determine a PMF with which to select the given actions.

        Args:
            context: The context we're currently in. See the base class for more information.
            actions: The actions to choose from. See the base class for more information.

        Returns:
            The probability of taking each action and information used for learning. See the base class for more information.
        """

        base_predicts = [ base_algorithm.predict(context, actions) for base_algorithm in self._base_learners ]
        base_predicts, base_infos = zip(*base_predicts)

        base_actions = [ self._random_pick.choice(actions, predict) for predict in base_predicts              ]
        base_probs   = [ predict[actions.index(action)] for action,predict in zip(base_actions,base_predicts) ]

        if self._type in ["importance"]:
            predict = [ sum([p_b*int(a==b_a) for p_b,b_a in zip(self._p_bars, base_actions)]) for a in actions ]
            info    = (base_actions, base_probs, base_infos, base_predicts, actions, predict)

        if self._type in ["off-policy", "rejection"]:
            predict = [ sum([p_b*b_p[i] for p_b,b_p in zip(self._p_bars, base_predicts)]) for i in range(len(actions)) ]
            info    = (base_actions, base_probs, base_infos, base_predicts, actions, predict)

        return (predict, info)

    def learn(self, context: Context, action: Action, reward: float, probability:float, info: Info) -> Dict[str, Any]:
        """Learn from the given interaction.

        Args:
            context: The context we're learning about. See the base class for more information.
            action: The action that was selected in the context. See the base class for more information.
            reward: The reward that was gained from the action. See the base class for more information.
            probability: The probability with which the given action was selected.
            info: Optional information provided during prediction step for use in learning.
        """

        assert  0 <= reward and reward <= 1, "This Corral implementation assumes a loss between 0 and 1"

        base_actions = info[0]
        base_probs   = info[1]
        base_infos   = info[2]
        base_preds   = info[3]
        actions      = info[4]
        predict      = info[5]

        base_learner_infos: Sequence[Optional[dict]] = []

        if self._type == "importance":
            # This is what is in the original paper. It has the following characteristics:
            #   > It is able to provide feedback to every base learner on every iteration
            #   > It uses a reward estimator with higher variance and no bias (aka, importance sampling)
            #   > It is "on-policy" with respect to base learner's prediction distributions
            # The reward, R, supplied to the base learners satisifies E[R|context,A] = E[reward|context,A]
            for learner, A, P, base_info in zip(self._base_learners, base_actions, base_probs, base_infos):
                R = reward * int(A==action)/probability
                base_learner_infos.append(learner.learn(context, A, R, P, base_info))

        if self._type == "off-policy":
            # An alternative variation to the paper is provided below. It has the following characterisitcs: 
            #   > It is able to provide feedback to every base learner on every iteration
            #   > It uses a MVUB reward estimator (aka, the unmodified, observed reward)
            #   > It is "off-policy" (i.e., base learners receive action feedback distributed differently from their predicts).
            for learner, base_info in zip(self._base_learners, base_infos):
                base_learner_infos.append(learner.learn(context, action, reward, probability, base_info))

        if self._type == "rejection":
            # An alternative variation to the paper is provided below. It has the following characterisitcs: 
            #   > It doesn't necessarily provide feedback to every base learner on every iteration
            #   > It uses a MVUB reward estimator (aka, the unmodified, observed reward) when it does provide feedback
            #   > It is "on-policy" (i.e., base learners receive action feedback is distributed identically to their predicts).
            p = self._random_reject.random() #can I reuse this across all learners like this??? I think so???
            for learner, base_info, base_predict in zip(self._base_learners, base_infos, base_preds):
                f = lambda a: base_predict[actions.index(a)] #the PMF we want
                g = lambda a: predict[actions.index(a)]      #the PMF we have
                
                M = max([f(A)/g(A) for A in actions if g(A) > 0])
                if p <= f(action)/(M*g(action)):
                    base_learner_infos.append(learner.learn(context, action, reward, f(action), base_info))

        # Instant loss is an unbiased estimate of E[loss|learner] for this iteration.
        # Our estimate differs from the orginal Corral paper because we have access to the
        # action probabilities of the base learners while the Corral paper did not assume 
        # access to this information. This information allows for a loss esimator with the same 
        # expectation as the original Corral paper's estimator but with a lower variance.

        loss = 1-reward

        picked_index = actions.index(action)
        instant_loss = [ loss * base_pred[picked_index]/probability for base_pred in base_preds ]
        self._ps     = CorralLearner._log_barrier_omd(self._ps, instant_loss, self._etas)
        self._p_bars = [ (1-self._gamma)*p + self._gamma*1/len(self._base_learners) for p in self._ps ]

        for i in range(len(self._base_learners)):
            if 1/self._p_bars[i] > self._rhos[i]:
                self._rhos[i] = 2/self._p_bars[i]
                self._etas[i] *= self._beta

        base_predict_data = { f"predict_{i}": base_preds[i][picked_index] for i in range(len(self._base_learners)) }
        base_pbar_data    = { f"pbar_{i}"   : self._p_bars[i]             for i in range(len(self._base_learners)) }
        predict_data      = { "predict"     : probability, **base_predict_data, **base_pbar_data }

        base_info = { k:v for b in filter(None,base_learner_infos) for k,v in b.items() }

        return { k:round(v,4) for k,v in {**predict_data, **base_predict_data, **base_pbar_data, **base_info}.items() }

    @staticmethod
    def _log_barrier_omd(ps, losses, etas) -> Sequence[float]:

        f  = lambda l: float(sum( [ 1/((1/p) + eta*(loss-l)) for p, eta, loss in zip(ps, etas, losses)]))
        df = lambda l: float(sum( [ eta/((1/p) + eta*(loss-l))**2 for p, eta, loss in zip(ps, etas, losses)]))

        denom_zeros = [ ((-1/p)-(eta*loss))/-eta for p, eta, loss in zip(ps, etas, losses) ]

        min_loss = min(losses)
        max_loss = max(losses)

        precision = 4

        def binary_search(l,r) -> Optional[float]:
            #in theory the above check should guarantee this has a solution
            while True:

                x = (l+r)/2
                y = f(x)

                if round(y,precision) == 1:
                    return x

                if y < 1:
                    l = x

                if y > 1:
                    r = x

        def find_root_of_1():
            brackets = list(sorted(filter(lambda z: min_loss <= z and z <= max_loss, set(denom_zeros + [min_loss, max_loss]))))

            for l_brack, r_brack in zip(brackets[:-1], brackets[1:]):
                
                if (f(l_brack+.00001)-1) * (f(r_brack-.00001)-1) >= 0:
                    continue
                else:
                    # we use binary search because newtons 
                    # method can overshoot our objective
                    return binary_search(l_brack, r_brack)

        lmbda: Optional[float] = None

        if min_loss == max_loss:
            lmbda = min_loss
        elif min_loss not in denom_zeros and round(f(min_loss),precision) == 1:
            lmbda = min_loss
        elif max_loss not in denom_zeros and round(f(max_loss),precision) == 1:
            lmbda = max_loss
        else:
            lmbda = find_root_of_1()

        if lmbda is None:
            raise Exception(f'Something went wrong in Corral OMD {ps}, {etas}, {losses}')

        new_ps = [ 1/((1/p) + eta*(loss-lmbda)) for p, eta, loss in zip(ps, etas, losses)]

        assert round(sum(new_ps),precision) == 1, "An invalid update was made by the log barrier in Corral"

        return new_ps