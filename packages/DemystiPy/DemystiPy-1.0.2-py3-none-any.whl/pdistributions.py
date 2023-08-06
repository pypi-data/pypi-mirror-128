from scipy.stats import binom, norm
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams["figure.figsize"] = (15,6)

class Binomial:
    
    def __init__(self):
        probabilities = None
        mean = None 
        var = None 
        
    def pmf(self,x,n,p,visualize=True,fill_color='orange'):

        r_values = list(range(n + 1))
        self.mean, self.var = binom.stats(n, p)

        self.probabilities = [binom.pmf(r, n, p) for r in r_values]

        prob_x = binom.pmf(x, n, p)
        
        if visualize:
            bars = plt.bar(r_values, self.probabilities)
            bars[x].set_color(fill_color)
            plt.xticks(r_values)
            plt.ylabel('Probability')
            plt.show()

        return prob_x
    
    def cdf(self,x,n,p,visualize=True,fill_color='orange',lower=False):

        r_values = list(range(n + 1))
        self.mean, self.var = binom.stats(n, p)

        self.probabilities = [binom.cdf(r, n, p) for r in r_values]

        prob_x = binom.cdf(x, n, p) if not lower else 1-binom.cdf(x, n, p)

        if visualize:
            bars = plt.bar(r_values, self.probabilities)
            if not lower:
                for i in range(x+1):
                    bars[i].set_color(fill_color)
            else:
                for i in range(x+1,n+1):
                    bars[i].set_color(fill_color)
            plt.xticks(r_values)
            plt.ylabel('Probability')
            plt.show()

        return prob_x
    
    def cdf2(self,x,n,p,visualize=True,fill_color='orange'):

        r_values = list(range(n + 1))
        self.mean, self.var = binom.stats(n, p)

        self.probabilities = [binom.cdf(r, n, p) for r in r_values]
        
        try:
            prob_x = binom.cdf(x[1], n, p) - binom.cdf(x[0], n, p)

            if visualize:
                bars = plt.bar(r_values, self.probabilities)
                for i in range(x[0],x[1]+1):
                    bars[i].set_color(fill_color)
                plt.xticks(r_values)
                plt.ylabel('Probability')
                plt.show()

            return prob_x
        
        except TypeError:
            raise TypeError("Input Parameter must be a list")


class Gaussian:
    
    def __init__(self):
        pass

    def cdf(self,x,mu,sigma,visualize=True,fill_color='lightblue',upper=False):

        prob = norm.cdf(x, mu, sigma) if not upper else 1-norm.cdf(x, mu, sigma)

        if visualize:
            s = np.random.normal(mu, sigma, 1000)
            s.sort()
            x = np.arange(s[0], x, 0.01) if not upper else np.arange(x, s[-1], 0.01)
            plt.plot(s, norm.pdf(s, mu, sigma))
            plt.ylabel('Probability')
            plt.fill_between(x, norm.pdf(x, mu, sigma),color=fill_color)

        return prob

    def cdf2(self,x,mu,sigma,visualize=True,fill_color='lightblue'):


        prob1 = norm.cdf(x[0], mu, sigma)
        prob2 = norm.cdf(x[1], mu, sigma)
        prob = prob2 - prob1


        if visualize:
            s = np.random.normal(mu, sigma, 1000)
            s.sort()
            x = np.arange(x[0], x[1], 0.01)
            plt.plot(s, norm.pdf(s, mu, sigma))
            plt.ylabel('Probability')
            plt.fill_between(x, norm.pdf(x, mu, sigma),color=fill_color)

        return prob
    
    def ppf(self,prob,mu,sigma,visualize=True,fill_color='lightblue'):
    
        val = norm.ppf(prob, mu, sigma)

        if visualize:
            s = np.random.normal(mu, sigma, 1000)
            s.sort()
            x = np.arange(s[0], val, 0.01)
            plt.plot(s, norm.pdf(s, mu, sigma))
            plt.ylabel('Probability')
            plt.fill_between(x, norm.pdf(x, mu, sigma),color=fill_color)

        return val