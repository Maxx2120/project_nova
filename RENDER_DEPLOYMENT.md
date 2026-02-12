# Deploy to Render.com

## Step 1: Create a Render Account
Go to [render.com](https://render.com) and sign up / log in.

## Step 2: Connect GitHub
1. In Render dashboard, click **New** → **Web Service**
2. Select **Connect a repository** → authorize GitHub
3. Find and select your `final-year-project` repo
4. Click **Connect**

## Step 3: Configure Web Service

| Field | Value |
|-------|-------|
| **Name** | `novaai-app` (or your choice) |
| **Environment** | `Python 3.11` |
| **Region** | `Oregon` (or closest to you) |
| **Branch** | `main` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn backend.main:app --host 0.0.0.0 --port $PORT` |
| **Plan** | Free (or Starter $12/month for more RAM) |

## Step 4: Set Environment Variables

Click **Environment** and add:

```
JWT_SECRET=your-super-secret-key-here-change-this
DATABASE_URL=sqlite:///./final_year_project.db
MODEL_HOST=http://<YOUR_GPU_VM_IP_OR_DOMAIN>:11434
PYTHONUNBUFFERED=true
```

Replace:
- `your-super-secret-key-here-change-this` → any random string (min 32 chars)
- `<YOUR_GPU_VM_IP_OR_DOMAIN>` → the IP/domain of your GPU VM (set up after this)

## Step 5: Deploy

Click **Create Web Service**. Render will:
1. Clone your repo from GitHub
2. Install dependencies
3. Start the app
4. Assign you a public URL like `https://novaai-app.onrender.com`

**Monitor logs:** In the Render dashboard, view the **Logs** tab to see if the app started successfully.

## Step 6: Verify Deployment

- Visit `https://novaai-app.onrender.com/`
- You should see the NovaAI landing page
- Signup / login should work
- Chat and image routes will fail until GPU VM is online (that's next)

## Step 7: Set Up GPU VM for Models

Once the web app is live on Render, provision a separate **GPU-enabled VM** with Ollama + Mistral + Stable Diffusion, and update `MODEL_HOST` in Render env vars to point to it.

See `GPU_VM_SETUP.sh` for detailed instructions.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Deployment fails | Check **Logs** tab for error. Common: missing `requirements.txt` or typo in start command. |
| App starts but 500 errors | MODEL_HOST not reachable. Verify GPU VM is online and firewall allows port 11434. |
| Database not persisting | Render free tier doesn't persist SQLite between deploys. Upgrade to Starter ($12/mo) or use managed DB. |
| Slow response times | Free tier has limited CPU. Upgrade to Starter or Starter Plus. |

## Auto-Deploy on Push

Render auto-redeploys when you push to GitHub `main` branch. To disable: Render dashboard → your service → Settings → toggle off **Auto-Deploy**.

---

**Next:** Set up your GPU VM using `GPU_VM_SETUP.sh`, then update `MODEL_HOST` in Render.
