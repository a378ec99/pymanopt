from __future__ import print_function, division

import time

from pymanopt.solvers.solver import Solver


class StochasticGradient(Solver):
    """
    Stochastic gradient algorithm based on
    stochasticgradient.m from the manopt MATLAB package.
    """

    def __init__(self, *args, **kwargs):
        super(StochasticGradient, self).__init__(*args, **kwargs)

    # Function to solve optimisation problem using stachastic gradient.
    def solve(self, problem, x=None):
        """
        Perform optimization using stochastic gradient.
        This method first computes the gradient (derivative) of obj
        w.r.t. arg based on a mini-batch of samples, and then optimizes by
        moving in the direction of ? with a step size rule based on ?.
        Arguments:
            - problem
                Pymanopt problem setup using the Problem class, this must
                have a .manifold attribute specifying the manifold to optimize
                over, as well as a cost and enough information to compute
                the gradient of that cost.
            - x=None
                Optional parameter. Starting point on the manifold. If none
                then a starting point will be randomly generated.
        Returns:
            - x
                Local minimum of obj, or if algorithm terminated before
                convergence x will be the point at which it terminated.
        """
        man = problem.manifold
        verbosity = problem.verbosity
        objective = problem.cost
        gradient = problem.grad

        # If no starting point is specified, generate one at random.
        if x is None:
            x = man.rand()

        # Initialize iteration counter and timer
        iter = 0
        time0 = time.time()

        if verbosity >= 2:
            print(" iter\t\t   cost val\t    grad. norm")

        self._start_optlog(extraiterfields=['gradnorm'],
                           solverparams={'linesearcher': linesearch})

        while True:

            # TODO sample without replacement a mini-batch and use it as x.

            # Calculate new cost, grad and gradnorm
            cost = objective(x)
            grad = gradient(x)
            gradnorm = man.norm(x, grad)
            iter = iter + 1

            if verbosity >= 2:
                print("%5d\t%+.16e\t%.8e" % (iter, cost, gradnorm))

            if self._logverbosity >= 2:
                self._append_optlog(iter, x, cost, gradnorm=gradnorm)

            # Descent direction is minus the gradient # WARNING What direction to use?
            desc_dir = -grad

            # Perform line-search
            stepsize, x = # TODO use step-size function to make step and return size.

            stop_reason = self._check_stopping_criterion(
                time0, stepsize=stepsize, gradnorm=gradnorm, iter=iter)

            if stop_reason:
                if verbosity >= 1:
                    print(stop_reason)
                    print('')
                break

        if self._logverbosity <= 0:
            return x
        else:
            self._stop_optlog(x, objective(x), stop_reason, time0,
                              stepsize=stepsize, gradnorm=gradnorm,
                              iter=iter)
            return x, self._optlog
