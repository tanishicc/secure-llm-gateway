from app.rate_limit import RateLimiter

def test_rate_limiter_blocks_after_threshold():
    rl = RateLimiter()
    # Patch the global settings used by the limiter module
    import app.config as config
    config.settings.max_requests_per_minute = 2

    assert rl.allow("c1", "1.1.1.1") is True
    assert rl.allow("c1", "1.1.1.1") is True
    assert rl.allow("c1", "1.1.1.1") is False
