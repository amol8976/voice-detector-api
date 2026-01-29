import secrets
print("vd_live_" + secrets.token_urlsafe(24))

import hashlib

key = "vd_live_EQqCtt984VYtkvuyVW0yjt9alW8CytI5"
print(hashlib.sha256(key.encode()).hexdigest())

