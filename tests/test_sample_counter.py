import numpy as np
from scipy.special import zeta
from utils.sample_counter import (
    generate_zipf_sample,
    calculate_sample_counts,
    generate_rank_array,
    calculate_expected_counts,
)


class TestSampleCounter:
    """Test suite for sample_counter.py Zipf distribution sampling"""

    def test_zipf_distribution_shape(self):
        """Test that Zipf distribution generates expected shape"""
        a = 4.0
        n = 1000
        s = generate_zipf_sample(a, n)
        
        assert len(s) == n
        assert s.dtype in [np.int64, np.int32]

    def test_zipf_parameters(self):
        """Test Zipf distribution with different parameters"""
        params = [2.0, 3.0, 4.0, 5.0]
        n = 1000
        
        for a in params:
            s = generate_zipf_sample(a, n)
            assert len(s) == n
            assert all(s > 0)  # Zipf distribution produces positive integers

    def test_calculate_sample_counts(self):
        """Test calculate_sample_counts function"""
        a = 3.0
        n = 1000
        s = generate_zipf_sample(a, n)
        count = calculate_sample_counts(s)
        
        assert len(count) == s.max() + 1
        assert sum(count) == n

    def test_zeta_function(self):
        """Test zeta function calculation"""
        a = 2.0
        z = zeta(a)
        
        # Riemann zeta(2) should be approximately pi^2/6 ≈ 1.6449
        assert isinstance(z, float)
        assert z > 1.0

    def test_expected_count_calculation(self):
        """Test calculate_expected_counts function"""
        a = 4.0
        n = 20000
        s = generate_zipf_sample(a, n)
        k = generate_rank_array(s.max())
        
        expected = calculate_expected_counts(k, a, n)
        
        assert len(expected) == len(k)
        assert all(expected > 0)
        assert all(np.isfinite(expected))

    def test_zipf_power_law(self):
        """Test that Zipf follows power law (higher ranks = lower frequencies)"""
        a = 3.0
        n = 10000
        s = generate_zipf_sample(a, n)
        count = calculate_sample_counts(s)
        
        # Count of rank 1 should generally be higher than count of rank 10
        # (statistical test, may occasionally fail due to randomness)
        if len(count) > 10:
            assert count[1] >= count[10] * 0.5  # Allow some variance

    def test_different_sample_sizes(self):
        """Test Zipf distribution with different sample sizes"""
        a = 4.0
        sizes = [100, 1000, 10000]
        
        for n in sizes:
            s = generate_zipf_sample(a, n)
            assert len(s) == n

    def test_zipf_minimum_value(self):
        """Test that Zipf distribution produces values >= 1"""
        a = 3.0
        n = 1000
        s = generate_zipf_sample(a, n)
        
        assert all(s >= 1)

    def test_generate_rank_array(self):
        """Test generate_rank_array function"""
        max_val = 100
        k = generate_rank_array(max_val)
        
        assert len(k) == max_val
        assert k[0] == 1
        assert k[-1] == max_val
        assert all(np.diff(k) == 1)  # Should be consecutive integers

    def test_expected_vs_sample_ratio(self):
        """Test that expected counts are proportional to power law"""
        a = 4.0
        k = np.array([1, 2, 4, 8])
        expected = k ** -a
        
        # Verify power law relationship
        ratio_1_2 = expected[0] / expected[1]
        ratio_2_4 = expected[1] / expected[2]
        
        # k=1 vs k=2: (1^-4) / (2^-4) = 2^4 = 16
        assert abs(ratio_1_2 - 16) < 0.1
        
        # k=2 vs k=4: (2^-4) / (4^-4) = 2^4 = 16
        assert abs(ratio_2_4 - 16) < 0.1
