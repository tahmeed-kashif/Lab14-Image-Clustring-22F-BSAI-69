# How to Deploy Your Project to the Web

To share your project with the world (and your professor), you need to put it on **GitHub** and then connect it to **Streamlit Cloud**.

## Step 1: Create a GitHub Repository
1. Go to [github.com](https://github.com/) and Log in (or Sign up).
2. Click the **+** icon in the top-right corner and select **New repository**.
3. Name it `Image-Clustering-Project`.
4. Make sure it is **Public**.
5. Click **Create repository**.

## Step 2: Push Your Code to GitHub
I have already prepared the local files for you. Now you just need to send them to GitHub.
1. Copy the commands shown on the GitHub page under **"…or push an existing repository from the command line"**.
2. It will look something like this (replace `YOUR_USERNAME` with your actual GitHub username):
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/Image-Clustering-Project.git
   git branch -M main
   git push -u origin main
   ```
3. Paste these commands into your terminal (where you are running the app) and hit Enter.

## Step 3: Deploy on Streamlit Cloud
1. Go back to your Streamlit app in the browser.
2. Click the **Deploy** button again.
3. Now that your code is on GitHub, it should automatically detect the repository.
4. Click **Deploy!**

## Troubleshooting
- If Streamlit asks for a "Main file path", enter: `app.py`
- If it asks for requirements, it will automatically find `requirements.txt`.

That's it! Your app will be live on the internet in a few minutes.
