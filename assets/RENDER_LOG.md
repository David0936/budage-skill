# Hero Animation Render Log

> 渲染日期：2026-05-10
> 工具链：huashu-design skill (Junior Designer 流程 · 简化版)
> 操作员：Claude Opus 4.7 (1M context)

## 交付物

| 文件 | 格式 | 规格 | 大小 |
|---|---|---|---|
| `hero.mp4` | MP4 | 1280×720 · 25fps · H.264 yuv420p · CRF 18 · faststart | 0.7 MB |
| `hero.gif` | GIF | 1024×576 · 15fps · palette 优化 (palettegen + bayer dither) | 4.1 MB |

GIF 实测 4.1 MB，低于 5 MB 目标且与张雪峰版 5.5 MB 同量级。MP4 仅 0.7 MB，远小于参考的"1-2 MB" 范围——因为画面以暗色 + 文字为主，H.264 压缩友好。

`hero-60fps.mp4`（740 KB，60fps 帧复制兼容版）也已生成，留在 `_render/` 工作区，未拷入 assets——README 只引用 `hero.gif`，60fps 版做交付候补，需要可单独取用。

## 风格 / Design Direction

**叙事结构**（10 秒，单镜头编年）：
1. **t=0.2-1.2s** · 顶部 kicker `ACT IV · ONE-MAN COMPANY MINDSET` 字距收紧 + 浮入
2. **t=0.8-2.2s** · `100` 三个数字逐位上推浮现（衬线大字 280px，0.3s stagger，expoOut easing）
3. **t=1.8-2.8s** · 数字下方爱马仕橙下划线从左向右 scaleX 揭示
4. **t=2.0-2.8s** · 上下副标签同步浮现（`日更条数 · CONDITIONS PER DAY` / `THE 100-A-DAY DOCTRINE · 用数量碾压算法`）
5. **t=3.0-5.4s** · 右侧 4 个彩色 tag 依次右滑入场（每张 0.45s 间隔，4 色错开：橙 → 金 → slate 蓝 → taupe）
6. **t=6.4-7.6s** · 底部金句「赚钱治百病。日更100条，把算法打懵。」浮现
7. **t=7.4-8.4s** · 底部署名 `CREATED BY HUASHU-DESIGN · 蒸馏自 NUWA-SKILL` 淡入
8. **t=0-10s** · 整个 stage 慢速 micro-zoom（1.000 → 1.018），cinematic 呼吸感

## 设计参数

- **配色**：`--bg-0: #0A0E1A`（深蓝近黑）→ `--bg-1: #1F2937`（深灰蓝）线性渐变 + 顶部橙色径向辉光（极淡）
- **致敬色**：`--accent: #F76707`（爱马仕橙——不答哥的标志性视觉符号），唯一 accent 串联：kicker dot、数字下划线、tag 1 边框、credit 间隔点
- **4 tag 配色**（按 task brief 用不同色彩区分）：橙 #F76707 / 金 #E8B14C / slate 蓝 #6B8DC7 / taupe #C9A87C，每个左 border + label color 配对
- **字体**：
  - 中央大数字：衬线（Source Han Serif SC / Noto Serif SC / Songti SC fallback chain，280px / -0.04em letter-spacing）
  - 中文正文 / 标签：PingFang SC / Source Han Sans SC
  - 拉丁小字（kicker / credit）：mono 字体，0.32-0.42em 大字距，符合"editorial / 数字纪实"调性
- **Editorial 细节**：
  - 四角 18px hairline 边框（`var(--ink-faint)`）—— 报纸 / 印刷品质感
  - 极淡 80px CSS grid，opacity 0.18，screen blend——背景纹理但不抢戏
  - 中央 vertical hairline scaleY 揭示——纵向锚点
- **Easing**：主体用 `expoOut`（爆发后阻尼），下划线用 `easeOutCubic`，与 hero-animation-case-study.md 推荐一致

## 工作流程实录

按 SKILL.md 走，做了如下取舍以满足 25 分钟时间预算：

1. **核心原则 #0 事实验证**：跳过——按 task 说明，不答哥本人数据已在 `budage.skill/SKILL.md` 可信记录
2. **核心资产协议**：走"无品牌资产"分支——
   - 不答哥是个人 IP，没有 logo（按 task 说明）
   - 致敬色 `#F76707`（爱马仕橙）作为唯一 accent
   - 字体走"通用现代中文设计语言"（思源宋 / 思源黑 系统字体 fallback chain）
3. **Junior Designer 模式**：直接进 Full pass——构图已由 task brief 锁死（顶部 kicker + 中央数字 + 右侧 tags + 底部 quote/credit），无需先 show assumption。先用 Playwright 在 4 个时间点截 PNG 验证布局，再录视频
4. **反 AI slop 自检**：通过——
   - 衬线大数字（不是 Inter / Roboto display）
   - 单 accent 色贯穿（不是紫渐变 / 多色聚类）
   - 诚实留白（无装饰 emoji / 无 CSS-绘人脸 / 无圆角左 border 卡片）
   - 暖橙微辉光替代赛博霓虹
5. **录制流水线**：
   - 自包含 HTML（无 React/Babel，纯 CSS + JS rAF loop）—— 渲染稳定性高于复杂栈
   - 实现 `window.__ready`（首帧 rAF 后置 true）+ `window.__seek(sec)`（pin time）+ `__recording` 检测（推断时禁 loop，最后一帧定格）
   - render-video.js 自动检测 ready 信号，trim=0.14s（auto），webm→H.264 yuv420p CRF 18
   - convert-formats.sh 派生 60fps 帧复制 + GIF（gif_width=1024，2-pass palette）

## 检查点

- ✅ 浏览器加载无 console error
- ✅ 第 0 帧 = 干净空场 stage（仅 editorial frame + 水印）
- ✅ 最后一帧 = 完整稳定收尾
- ✅ 字体渲染正常（中文宋体 + mono Latin）
- ✅ Duration 10s 与 timeline T.end=10.0 匹配
- ✅ `__recording=true` 时 loop 禁用（render() 在 t > end 后定格 final frame）
- ✅ 含「Created by Huashu-Design」水印（右下，10px 字号 0.30 透明度）

## 偏离 / 妥协

1. **未加 BGM/SFX**：task brief 标"音乐可选 + 克制"，且 25 分钟预算内 BGM/SFX 双轨制+频段隔离会挤压时间——交付为纯画面 MP4。如需配乐，后续可单独跑 `add-music.sh hero.mp4 --mood=tech` 一键加默认 Apple Silicon 风格 BGM
2. **未启用 minterpolate 真插帧**：默认走帧复制兼容模式（QuickTime / Safari / 微信都能播），如需 B 站等真插帧场景，加 `--minterpolate` 参数重跑
3. **分辨率 1280×720 而非 1920×1080**：按 task 明确要求 1280×720。这也让 GIF 体积更友好
4. **未走完整 product-facts.md / brand-spec.md 文件落盘**：按 task 说明跳过——所有数据/资产在 `budage.skill/SKILL.md` 已记录，再写一份会是重复劳动

## 没遇到的问题

- Playwright 全局未装 → 已 `npm install -g playwright`（chromium 已存在于 ~/Library/Caches/ms-playwright/，无需 download）
- 首次截图 `__seek(7.5)` 后画面被 rAF loop 重置为 t=0 → 已修：引入 `pinnedTime` 变量，tick 在 pinned 状态下持续渲染该时间，`__recording=true` 时通过 setInterval 自动解锁，恢复正常播放

## 工作区残留

`/Users/david/Documents/公众号/David小鱼/05 不答哥/_render/` 保留了：
- `hero.html`（源 HTML，可双击预览）
- `hero.mp4` / `hero-60fps.mp4` / `hero.gif`（与 assets 同名 + 60fps 候补版）
- `frame-*.png` / `mp4-check.png` / `mp4-start.png`（验证截帧）
- `screenshot_check.js`（Playwright 检查脚本）

主 agent 如不需要可整目录清理，不影响 budage.skill/assets/ 交付物。
