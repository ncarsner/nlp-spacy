import matplotlib.pyplot as plt
import numpy as np
from scipy.special import zeta


def generate_zipf_sample(a, n):
    """
    Generate a Zipf distribution sample.
    
    Args:
        a: Zipf parameter (power law exponent)
        n: Sample size
        
    Returns:
        numpy array of Zipf-distributed random integers
    """
    return np.random.zipf(a, n)


def calculate_sample_counts(sample):
    """
    Calculate frequency counts for each unique value in sample.
    
    Args:
        sample: Array of integer values
        
    Returns:
        Array where index i contains the count of value i in the sample
    """
    return np.bincount(sample)


def generate_rank_array(max_value):
    """
    Generate array of ranks from 1 to max_value.
    
    Args:
        max_value: Maximum rank value
        
    Returns:
        Array of integers from 1 to max_value
    """
    return np.arange(1, max_value + 1)


def calculate_expected_counts(k, a, n):
    """
    Calculate expected counts for Zipf distribution.
    
    Args:
        k: Array of ranks
        a: Zipf parameter
        n: Total sample size
        
    Returns:
        Array of expected counts for each rank
    """
    return n * (k ** -a) / zeta(a)


def plot_zipf_comparison(k, sample_counts, expected_counts, a, n):
    """
    Plot comparison of sample counts vs expected Zipf distribution.
    
    Args:
        k: Array of ranks
        sample_counts: Actual counts from sample
        expected_counts: Expected counts from theory
        a: Zipf parameter
        n: Sample size
    """
    plt.bar(k, sample_counts[1:], alpha=0.5, label="sample count")
    plt.plot(k, expected_counts, "k.-", alpha=0.5, label="expected count")
    plt.semilogy()
    plt.grid(alpha=0.4)
    plt.legend()
    plt.title(f"Zipf sample, a={a}, size={n}")
    plt.show()


def main():
    """Main function for Zipf sampling and visualization."""
    a = 4.0
    n = 20_000
    
    s = generate_zipf_sample(a, n)
    count = calculate_sample_counts(s)
    k = generate_rank_array(s.max())
    expected = calculate_expected_counts(k, a, n)
    
    plot_zipf_comparison(k, count, expected, a, n)


if __name__ == "__main__":
    main()
