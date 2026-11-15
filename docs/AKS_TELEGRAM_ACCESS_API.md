# АКС — API выдачи доступа через Telegram (для программиста бота)

Статус: Edge Function развернута, **не готова к использованию до настройки секретов и теста**.

Endpoint: `POST https://dlpkuifrymxejmhemykm.supabase.co/functions/v1/aks-telegram-access`

Headers:
```
Authorization: Bearer <AKS_BOT_API_TOKEN>
Content-Type: application/json
```

Body:
```json
{"action":"get_access","telegram_id":123456789}
```

Successful first issuance (201):
```json
{"login":"aks12345678","password":"abcdefgh","created":true}
```

Repeated issuance (200): same `login` and `password`, `created:false`.

Errors: 400 invalid_request; 401 unauthorized; 403 account_disabled; 409 credentials_unavailable; 503 not_configured/retry_later; 500 internal_error. Password shown above is an example, not a real credential.

**Bot responsibilities:**
- Only call this endpoint from the trusted bot backend, never from a client/browser.
- Derive `telegram_id` from the Telegram update's authenticated `from.id`, never from user-entered text.
- Before every call verify that the sender is an existing eligible employee in the bot's own 1C-linked employee database. A Telegram ID by itself is NOT authorization. The API trusts the bot to do this check.
- Add button «Получить доступ к сайту»; respond with the returned login/password via private Telegram chat only.
- Do not log passwords, request/response bodies, or API tokens. Avoid forwarding to group chats. Rate-limit requests and avoid simultaneous calls for the same ID.
- Do not call on behalf of an arbitrary ID. If employee access is revoked, coordinate blocking `enabled=false` and Auth sessions with site administrators.
- Do not change passwords automatically on repeat clicks; do not create duplicate accounts.

**Supabase project owner setup required BEFORE testing:**
- Configure Edge Function secrets `AKS_BOT_API_TOKEN` (cryptographically random >=32 characters) and `AKS_CREDENTIAL_ENCRYPTION_KEY` (base64-encoded 32 random bytes) in Supabase Dashboard > Edge Functions > Secrets.
- Keep both secret values outside GitHub, Telegram chat, and browser code. Give the bot programmer only the bot API token via a secure private channel.
- Supabase supplies `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` to functions; confirm their availability.
- **Back up the encryption key securely**: losing it makes old passwords unrecoverable for repeated delivery. Rotating it requires re-encrypting saved credentials.
- After configuring secrets, test first/repeat issuance with a dedicated test Telegram ID, verify same credentials, verify 401 for missing token and 403 for blocked account. Do not use real employees for initial tests.

**Site login implementation is a separate stage.** The backend uses Supabase Auth with internal email `<login>@aks.invalid`; site login form will translate the user-facing login to that internal email and call Supabase Auth signInWithPassword. Employee role must not confer admin privileges.

GitHub Pages is public: this login is only a UI gate and does not protect static assets or directly linked product files.
