from flask import Flask, request, jsonify, Response
import yt_dlp

app = Flask(__name__)

INDEX_HTML = """<!DOCTYPE html>
<html lang="bn">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>YouTube Video Downloader</title>
<script src="https://cdn.tailwindcss.com"></script>
<style>
  body { font-family: 'Segoe UI', sans-serif; }
  .spinner { border-top-color: transparent; }
</style>
</head>
<body class="bg-gradient-to-br from-red-50 via-white to-red-100 min-h-screen">
  <div class="max-w-2xl mx-auto px-4 py-10">
    <div class="text-center mb-8">
      <h1 class="text-3xl md:text-4xl font-bold text-gray-800">📥 YouTube Video Downloader</h1>
      <p class="text-gray-500 mt-2">যেকোনো YouTube ভিডিও লিংক পেস্ট করুন এবং ডাউনলোড করুন</p>
    </div>

    <div class="bg-white rounded-2xl shadow-lg p-6">
      <div class="flex flex-col sm:flex-row gap-3">
        <input id="urlInput" type="text" placeholder="YouTube ভিডিও লিংক পেস্ট করুন..."
          class="flex-1 border border-gray-300 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-red-400">
        <button id="fetchBtn" onclick="fetchInfo()"
          class="bg-red-600 hover:bg-red-700 text-white font-semibold px-6 py-3 rounded-xl transition">
          খুঁজুন
        </button>
      </div>
      <div id="status" class="mt-4 text-sm"></div>

      <div id="result" class="mt-6 hidden">
        <div class="flex gap-4 items-start">
          <img id="thumb" class="w-40 rounded-xl shadow" src="" alt="thumbnail">
          <div>
            <h2 id="videoTitle" class="font-semibold text-gray-800 text-lg"></h2>
            <p id="videoDuration" class="text-gray-500 text-sm mt-1"></p>
          </div>
        </div>
        <div id="formats" class="mt-5 space-y-2"></div>
      </div>
    </div>

    <p class="text-center text-xs text-gray-400 mt-8">
      শুধুমাত্র নিজস্ব বা কপিরাইট-মুক্ত কন্টেন্ট ডাউনলোডের জন্য ব্যবহার করুন।
    </p>
  </div>

<script>
async function fetchInfo() {
  const url = document.getElementById('urlInput').value.trim();
  const status = document.getElementById('status');
  const result = document.getElementById('result');
  const formatsDiv = document.getElementById('formats');
  result.classList.add('hidden');
  formatsDiv.innerHTML = '';

  if (!url) {
    status.innerHTML = '<span class="text-red-500">অনুগ্রহ করে একটি লিংক দিন</span>';
    return;
  }

  status.innerHTML = '<span class="text-gray-500">তথ্য সংগ্রহ করা হচ্ছে...</span>';

  try {
    const res = await fetch('/api/info', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url })
    });
    const data = await res.json();

    if (data.error) {
      status.innerHTML = `<span class="text-red-500">ত্রুটি: ${data.error}</span>`;
      return;
    }

    status.innerHTML = '';
    document.getElementById('thumb').src = data.thumbnail || '';
    document.getElementById('videoTitle').innerText = data.title || '';
    const mins = Math.floor((data.duration || 0) / 60);
    const secs = (data.duration || 0) % 60;
    document.getElementById('videoDuration').innerText = `⏱ ${mins}:${secs.toString().padStart(2,'0')}`;

    if (!data.formats || data.formats.length === 0) {
      formatsDiv.innerHTML = '<p class="text-gray-500">কোনো ডাউনলোডযোগ্য ফরম্যাট পাওয়া যায়নি</p>';
    } else {
      data.formats.forEach(f => {
        const sizeMB = f.filesize ? (f.filesize / (1024*1024)).toFixed(1) + ' MB' : 'আনুমানিক আকার নেই';
        const row = document.createElement('div');
        row.className = 'flex items-center justify-between border rounded-xl px-4 py-3';
        row.innerHTML = `
          <div>
            <p class="font-medium text-gray-700">${f.resolution || f.ext} <span class="text-xs text-gray-400">(${f.ext})</span></p>
            <p class="text-xs text-gray-400">${sizeMB}</p>
          </div>
          <button class="bg-gray-800 hover:bg-black text-white text-sm px-4 py-2 rounded-lg"
            onclick="downloadFormat('${f.format_id}')">ডাউনলোড</button>
        `;
        formatsDiv.appendChild(row);
      });
    }

    result.classList.remove('hidden');
  } catch (err) {
    status.innerHTML = `<span class="text-red-500">সার্ভার ত্রুটি: ${err.message}</span>`;
  }
}

async function downloadFormat(formatId) {
  const url = document.getElementById('urlInput').value.trim();
  const status = document.getElementById('status');
  status.innerHTML = '<span class="text-gray-500">ডাউনলোড লিংক তৈরি হচ্ছে...</span>';

  try {
    const res = await fetch('/api/download', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url, format_id: formatId })
    });
    const data = await res.json();

    if (data.error) {
      status.innerHTML = `<span class="text-red-500">ত্রুটি: ${data.error}</span>`;
      return;
    }

    status.innerHTML = '<span class="text-green-600">লিংক প্রস্তুত, ডাউনলোড শুরু হচ্ছে...</span>';
    window.open(data.download_url, '_blank');
  } catch (err) {
    status.innerHTML = `<span class="text-red-500">সার্ভার ত্রুটি: ${err.message}</span>`;
  }
}
</script>
</body>
</html>
"""


@app.route("/")
def index():
    return Response(INDEX_HTML, mimetype="text/html")


@app.route("/api/info", methods=["POST"])
def info():
    data = request.get_json(silent=True) or {}
    url = data.get("url")
    if not url:
        return jsonify({"error": "URL প্রয়োজন"}), 400

    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "noplaylist": True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            video_info = ydl.extract_info(url, download=False)

        formats = []
        for f in video_info.get("formats", []):
            # শুধু ভিডিও+অডিও একসাথে থাকা ফরম্যাটগুলো নেওয়া হচ্ছে
            # (ffmpeg ছাড়া merge করার প্রয়োজন এড়াতে)
            if f.get("vcodec") != "none" and f.get("acodec") != "none" and f.get("url"):
                formats.append({
                    "format_id": f.get("format_id"),
                    "ext": f.get("ext"),
                    "resolution": f.get("format_note") or f.get("resolution"),
                    "filesize": f.get("filesize") or f.get("filesize_approx"),
                })

        return jsonify({
            "title": video_info.get("title"),
            "thumbnail": video_info.get("thumbnail"),
            "duration": video_info.get("duration"),
            "formats": formats,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/download", methods=["POST"])
def download():
    data = request.get_json(silent=True) or {}
    url = data.get("url")
    format_id = data.get("format_id")
    if not url or not format_id:
        return jsonify({"error": "URL এবং format_id প্রয়োজন"}), 400

    try:
        ydl_opts = {
            "quiet": True,
            "format": format_id,
            "noplaylist": True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            video_info = ydl.extract_info(url, download=False)

        direct_url = video_info.get("url")
        if not direct_url:
            return jsonify({"error": "ডাউনলোড লিংক পাওয়া যায়নি"}), 500

        return jsonify({
            "download_url": direct_url,
            "title": video_info.get("title"),
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
