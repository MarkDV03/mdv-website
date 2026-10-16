// Local preview server: node serve.js  ->  http://localhost:5173
const http = require("http");
const fs = require("fs");
const path = require("path");
const zlib = require("zlib");

const PORT = process.env.PORT || 5173;
const ROOT = __dirname;
const TYPES = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".webp": "image/webp",
  ".ico": "image/x-icon",
  ".txt": "text/plain; charset=utf-8",
  ".xml": "application/xml; charset=utf-8",
};

function send(res, status, file) {
  fs.readFile(file, (err, data) => {
    if (err) {
      res.writeHead(404, { "Content-Type": "text/plain" });
      return res.end("Not found");
    }
    const type = TYPES[path.extname(file).toLowerCase()] || "application/octet-stream";
    const gzip = /text|javascript|svg|xml|json/.test(type) && /gzip/.test(res.req.headers["accept-encoding"] || "");
    res.writeHead(status, gzip ? { "Content-Type": type, "Content-Encoding": "gzip" } : { "Content-Type": type });
    res.end(gzip ? zlib.gzipSync(data) : data);
  });
}

http
  .createServer((req, res) => {
    // Netlify handles form posts in production; locally we just pretend it worked.
    if (req.method === "POST") {
      req.resume();
      req.on("end", () => {
        if ((req.headers["content-type"] || "").includes("urlencoded") && req.headers["accept"] && !req.headers["accept"].includes("text/html")) {
          res.writeHead(200, { "Content-Type": "text/plain" });
          return res.end("ok");
        }
        res.writeHead(303, { Location: "/thanks.html" });
        res.end();
      });
      return;
    }
    let urlPath = decodeURIComponent(req.url.split("?")[0]);
    if (urlPath.endsWith("/")) urlPath += "index.html";
    const file = path.normalize(path.join(ROOT, urlPath));
    if (!file.startsWith(ROOT)) {
      res.writeHead(403);
      return res.end();
    }
    fs.stat(file, (err, stat) => {
      if (!err && stat.isFile()) return send(res, 200, file);
      send(res, 404, path.join(ROOT, "404.html"));
    });
  })
  .listen(PORT, () => console.log(`MDV Web Design preview: http://localhost:${PORT}`));
