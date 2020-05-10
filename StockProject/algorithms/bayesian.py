import numpy as np

def polynomial(X, M):
    phi = np.array([X ** i for i in range(M)]).T
    return phi


def identity(X, M):
    phi = np.array([X for _ in range(M)]).T
    return phi


def gaussian(X, mu_list, sigma_list=None):
    if sigma_list is None:
        sigma_list = [0.1]
    f = lambda x, mu, sigma: np.exp(-0.5 * (x - mu) ** 2 / sigma ** 2)
    phi = []
    for x in X:
        phi_list = [x]
        for mu in mu_list:
            for sigma in sigma_list:
                phi_list.append(f(x, mu, sigma))
        phi.append(phi_list)
    phi = np.array(phi)
    return phi


class BayesianModel():
    def __init__(self, alpha=1e-5, beta=1e-5):
        """
        Construction of Bayesian model.

        Args:
            alpha: Single value parameter.
            beta: Single value parameter.
            m: Mean of the posterior distribution.
            S: Covariance matrix of the posterior distribution.
        """
        self.alpha = alpha
        self.beta = beta
        self.m = None
        self.S = None

    def posterior(self, phi, t):
        """
        Computes mean and covariance matrix of the posterior distribution.
        Args:
            phi: Design matrix (N x M).
            t: Target vector (N).
        Returns:
            m: Mean of the posterior distribution (M).
            S: Covariance matrix of the posterior distribution (M x M).
            S_inv: Inverse of S (M x M).
        """
        S_inv = self.alpha * np.eye(phi.shape[1]) + self.beta * phi.T.dot(phi)  # 1.72
        S = np.linalg.inv(S_inv)
        m = self.beta * S.dot(phi.T).dot(t)  # 1.70
        return m, S, S_inv

    def fit(self, phi, t, max_iter=200, rtol=1e-12, verbose=False):
        """
        Jointly infers the posterior sufficient statistics and optimal values
        for alpha and beta by maximizing the log marginal likelihood.

        Args:
            phi: Design matrix (N x M).
            t: Target value array (N x 1).
            max_iter: Maximum number of iterations.
            rtol: Convergence criterion.

        Returns:
            posterior mean, posterior covariance.
        """
        N, M = phi.shape
        eigen_0 = np.linalg.eigvalsh(phi.T.dot(phi))
        for iter in range(max_iter):
            pre_beta = self.beta
            pre_alpha = self.alpha
            eigen = eigen_0 * self.beta
            m, S, S_inv = self.posterior(phi, t)
            gamma = np.sum(eigen / (eigen + self.alpha))
            self.alpha = gamma / np.sum(m ** 2)
            beta_inv = 1 / (N - gamma) * np.sum((t - phi.dot(m)) ** 2)
            self.beta = 1 / beta_inv
            if np.isclose(pre_alpha, self.alpha, rtol=rtol) and np.isclose(pre_beta, self.beta, rtol=rtol):
                if verbose:
                    print(f'alpha:{self.alpha} beta:{self.beta}')
                    print(f'Convergence after {iter + 1} iterations.')
                self.m, self.S = m, S
                return
            if verbose:
                print(f'alpha:{self.alpha} beta:{self.beta}')
        if verbose:
            print(f'Stopped after {max_iter} iterations.')
        self.m, self.S = m, S

    def predict(self, phi_):
        """
        Computes mean and variances of the posterior predictive distribution.
        Args:
            phi_: Design matrix of test input x (M).
        Returns:
            y: Mean of the posterior predictive distribution.
            y_var: Variances of the posterior predictive distribution (M x M).
        """
        y = phi_.dot(self.m)  # pick the mean of the distribution to predict the target
        y_var = 1 / self.beta + np.sum(phi_.dot(self.S) * phi_, axis=1)  # 1.71
        return y, y_var

if __name__ == '__main__':
    X_original, t_original = load_data(args.file)
    train_limit = 100
    X = X_original / (train_limit + 1)
    X_test = X[:train_limit+1]
    X = X[:train_limit]
    t = t_original[:train_limit]
    M = 32

    mu_list = np.linspace(0, 1, M)
    sigma_list = [0.1 ** i for i in range(1, 5)]
    phi = gaussian(X, mu_list, sigma_list)
    phi_test = gaussian(X_test, mu_list, sigma_list)

    model = BayesianModel()
    model.fit(phi, t, verbose=True)
    t_predicted, t_var = model.predict(phi_test)
    # performance(t_original, t_predicted)
    plot(X_original, t_original, t_predicted, train_limit)