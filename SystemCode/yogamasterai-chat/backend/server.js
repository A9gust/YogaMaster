const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const { exec } = require('child_process');

const app = express();
const PORT = 8000;

app.use(bodyParser.json());
app.use(cors());

app.post('/chat', (req, res) => {
    const userMessage = req.body.message;

    // 使用 Python 脚本处理消息
    exec(`python chat.py "${userMessage}"`, (error, stdout, stderr) => {
        if (error) {
            console.error(`执行错误: ${error.message}`);
            return res.status(500).json({ error: "内部服务器错误" });
        }
        if (stderr) {
            console.error(`错误输出: ${stderr}`);
            return res.status(500).json({ error: "处理错误" });
        }

        // 返回 Python 脚本的输出
        res.json({ response: stdout.trim() });
    });
});

app.listen(PORT, () => {
    console.log(`服务器正在运行，端口：${PORT}`);
});
