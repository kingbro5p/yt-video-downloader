# YouTube Video Downloader

Python (Flask + yt-dlp) দিয়ে তৈরি একটি YouTube Video Downloader ওয়েবসাইট। Vercel-এ সরাসরি ডিপ্লয়যোগ্য।

## ফিচার
- YouTube লিংক পেস্ট করে ভিডিওর তথ্য (থাম্বনেইল, টাইটেল, দৈর্ঘ্য) দেখা
- একাধিক রেজোলিউশন/ফরম্যাট থেকে বেছে নিয়ে ডাউনলোড লিংক তৈরি করা
- সম্পূর্ণ সার্ভারলেস (Vercel Python Function)

## GitHub-এ আপলোড করবেন যেভাবে
1. এই zip ফাইলটি extract করুন
2. GitHub-এ একটি নতুন রিপোজিটরি তৈরি করুন (যেমন `youtube-downloader`)
3. টার্মিনালে extract করা ফোল্ডারে গিয়ে চালান:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<repo-name>.git
   git push -u origin main
   ```

## Vercel-এ ডিপ্লয় করবেন যেভাবে
1. [vercel.com](https://vercel.com) এ লগইন করুন (GitHub দিয়ে লগইন করাই সহজ)
2. "Add New Project" → আপনার GitHub রিপোজিটরি সিলেক্ট করুন
3. Framework Preset: **Other** রাখুন (vercel.json নিজেই কনফিগারেশন হ্যান্ডেল করবে)
4. Deploy চাপুন — কয়েক মিনিটেই আপনার লাইভ লিংক পেয়ে যাবেন

## গুরুত্বপূর্ণ নোট
- এই টুলটি শুধুমাত্র **নিজের তৈরি করা বা কপিরাইট-মুক্ত/অনুমতিপ্রাপ্ত কন্টেন্ট** ডাউনলোডের জন্য ব্যবহার করা উচিত। অন্যের কপিরাইটযুক্ত ভিডিও অনুমতি ছাড়া ডাউনলোড করা YouTube-এর শর্তাবলী ও কপিরাইট আইন লঙ্ঘন করতে পারে।
- Vercel-এর Hobby প্ল্যানে সার্ভারলেস ফাংশনের সময়সীমা সীমিত (১০ সেকেন্ড), তাই খুব দীর্ঘ ভিডিওর ক্ষেত্রে তথ্য আনতে সময় বেশি লাগলে টাইমআউট হতে পারে।
- এই ভার্সনে ভিডিও ফাইল সরাসরি Vercel সার্ভারে সংরক্ষণ হয় না — ব্যবহারকারীকে YouTube-এর নিজস্ব CDN থেকে সরাসরি ডাউনলোড লিংক দেওয়া হয়, যা সার্ভারলেস পরিবেশের জন্য উপযোগী।

## লোকাল টেস্টিং
```bash
pip install -r requirements.txt
python api/index.py
```
তারপর ব্রাউজারে `http://localhost:5000` ভিজিট করুন।
