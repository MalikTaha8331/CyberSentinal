const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';
pres.title = 'CyberSentinel - AI Intrusion Detection & Prevention System';

// ─── Color Palette ─────────────────────────────────
const C = {
    bg:       '05050F',
    card:     '0D0D1F',
    purple:   '9D4EDD',
    gold:     'FFD700',
    green:    '00FF88',
    red:      'FF2255',
    cyan:     '00E5FF',
    gray:     '8888AA',
    white:    'FFFFFF',
    darkPurp: '1A0A2E',
    midPurp:  '2D1B69',
};

const makeShadow = () => ({ type: "outer", blur: 8, offset: 3, angle: 135, color: "000000", opacity: 0.3 });

// ══════════════════════════════════════════════════
// SLIDE 1 — Title
// ══════════════════════════════════════════════════
{
    const s = pres.addSlide();
    s.background = { color: C.bg };

    // Background glow shapes
    s.addShape(pres.shapes.OVAL, { x: -1, y: -1, w: 5, h: 5, fill: { color: C.purple, transparency: 88 }, line: { color: C.purple, transparency: 88 } });
    s.addShape(pres.shapes.OVAL, { x: 7, y: 2, w: 4, h: 4, fill: { color: C.gold, transparency: 92 }, line: { color: C.gold, transparency: 92 } });

    // Top accent bar
    s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.04, fill: { color: C.purple }, line: { color: C.purple } });
    s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0.04, w: 10, h: 0.04, fill: { color: C.gold }, line: { color: C.gold } });

    // Sword icon text
    s.addText('⚔️', { x: 4.3, y: 0.7, w: 1.4, h: 1.0, fontSize: 48, align: 'center' });

    // Title
    s.addText('CYBERSENTINEL', {
        x: 0.5, y: 1.55, w: 9, h: 1.1,
        fontSize: 52, bold: true, color: C.gold,
        align: 'center', fontFace: 'Arial Black', charSpacing: 6, margin: 0
    });

    // Subtitle
    s.addText('AI-Powered Intrusion Detection & Prevention System', {
        x: 0.5, y: 2.7, w: 9, h: 0.5,
        fontSize: 16, color: C.gray, align: 'center',
        fontFace: 'Calibri', charSpacing: 2, margin: 0
    });

    // Divider
    s.addShape(pres.shapes.RECTANGLE, { x: 3.5, y: 3.3, w: 3, h: 0.03, fill: { color: C.purple }, line: { color: C.purple } });

    // Three key stats
    const stats = [
        { label: '99.92%', sub: 'Model Accuracy', x: 1.0 },
        { label: 'Real-Time', sub: 'Threat Detection', x: 4.0 },
        { label: 'Auto-Block', sub: 'Severe Threats', x: 7.0 },
    ];

    stats.forEach(st => {
        s.addShape(pres.shapes.RECTANGLE, { x: st.x, y: 3.55, w: 2.0, h: 1.2, fill: { color: C.card }, line: { color: C.midPurp }, shadow: makeShadow() });
        s.addText(st.label, { x: st.x, y: 3.6, w: 2.0, h: 0.55, fontSize: 18, bold: true, color: C.gold, align: 'center', fontFace: 'Arial Black', margin: 0 });
        s.addText(st.sub, { x: st.x, y: 4.15, w: 2.0, h: 0.4, fontSize: 10, color: C.gray, align: 'center', fontFace: 'Calibri', margin: 0 });
    });

    // Bottom bar
    s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 5.58, w: 10, h: 0.04, fill: { color: C.gold }, line: { color: C.gold } });
    s.addText('Final Year Project  |  BS Cybersecurity  |  2025-2026', {
        x: 0, y: 5.28, w: 10, h: 0.3, fontSize: 9, color: C.gray, align: 'center', fontFace: 'Calibri', margin: 0
    });
}

// ══════════════════════════════════════════════════
// SLIDE 2 — Problem & Solution
// ══════════════════════════════════════════════════
{
    const s = pres.addSlide();
    s.background = { color: C.bg };

    s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.04, fill: { color: C.purple }, line: { color: C.purple } });

    s.addText('THE PROBLEM & OUR SOLUTION', {
        x: 0.4, y: 0.15, w: 9.2, h: 0.55,
        fontSize: 22, bold: true, color: C.gold,
        fontFace: 'Arial Black', charSpacing: 3, margin: 0
    });

    // Problem side
    s.addShape(pres.shapes.RECTANGLE, { x: 0.3, y: 0.85, w: 4.3, h: 4.3, fill: { color: C.card }, line: { color: 'FF2255' }, shadow: makeShadow() });
    s.addText('❌  THE PROBLEM', { x: 0.3, y: 0.85, w: 4.3, h: 0.5, fontSize: 13, bold: true, color: 'FF2255', align: 'center', fontFace: 'Arial Black', margin: 0 });

    const problems = [
        'Traditional systems use fixed rules',
        'Cannot detect new unknown attacks',
        'Require constant manual updates',
        'High false positive rates',
        'No automatic blocking capability',
        'Slow response to threats',
    ];

    s.addText(problems.map((p, i) => ({
        text: p,
        options: { bullet: true, color: C.gray, fontSize: 12, fontFace: 'Calibri', breakLine: i < problems.length - 1, paraSpaceAfter: 6 }
    })), { x: 0.5, y: 1.45, w: 3.9, h: 3.5 });

    // Solution side
    s.addShape(pres.shapes.RECTANGLE, { x: 5.4, y: 0.85, w: 4.3, h: 4.3, fill: { color: C.card }, line: { color: C.green }, shadow: makeShadow() });
    s.addText('✅  OUR SOLUTION', { x: 5.4, y: 0.85, w: 4.3, h: 0.5, fontSize: 13, bold: true, color: C.green, align: 'center', fontFace: 'Arial Black', margin: 0 });

    const solutions = [
        'AI learns attack patterns from data',
        'Detects zero-day unknown attacks',
        'Self-updating ML model',
        '99.92% accuracy on NSL-KDD',
        'Auto-blocks severe threats instantly',
        'Real-time alerts on live dashboard',
    ];

    s.addText(solutions.map((p, i) => ({
        text: p,
        options: { bullet: true, color: C.gray, fontSize: 12, fontFace: 'Calibri', breakLine: i < solutions.length - 1, paraSpaceAfter: 6 }
    })), { x: 5.6, y: 1.45, w: 3.9, h: 3.5 });

    // VS circle
    s.addShape(pres.shapes.OVAL, { x: 4.5, y: 2.6, w: 0.9, h: 0.9, fill: { color: C.purple }, line: { color: C.gold } });
    s.addText('VS', { x: 4.5, y: 2.6, w: 0.9, h: 0.9, fontSize: 13, bold: true, color: C.gold, align: 'center', valign: 'middle', fontFace: 'Arial Black', margin: 0 });

    s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 5.58, w: 10, h: 0.04, fill: { color: C.gold }, line: { color: C.gold } });
}

// ══════════════════════════════════════════════════
// SLIDE 3 — System Architecture
// ══════════════════════════════════════════════════
{
    const s = pres.addSlide();
    s.background = { color: C.bg };

    s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.04, fill: { color: C.purple }, line: { color: C.purple } });

    s.addText('SYSTEM ARCHITECTURE', {
        x: 0.4, y: 0.15, w: 9.2, h: 0.55,
        fontSize: 22, bold: true, color: C.gold,
        fontFace: 'Arial Black', charSpacing: 3, margin: 0
    });

    // Pipeline steps
    const steps = [
        { icon: '📡', title: 'CAPTURE', desc: 'Scapy sniffs\nlive packets', color: C.cyan },
        { icon: '🔬', title: 'EXTRACT', desc: '41 NSL-KDD\nfeatures', color: C.purple },
        { icon: '🤖', title: 'CLASSIFY', desc: 'Random Forest\nML model', color: C.gold },
        { icon: '⚠️', title: 'CATEGORIZE', desc: '4-tier threat\nlevels', color: 'FF8800' },
        { icon: '🚫', title: 'ACT', desc: 'Alert & auto\nblock threats', color: C.red },
    ];

    steps.forEach((st, i) => {
        const x = 0.3 + i * 1.9;
        s.addShape(pres.shapes.RECTANGLE, { x, y: 0.95, w: 1.6, h: 2.4, fill: { color: C.card }, line: { color: st.color }, shadow: makeShadow() });
        s.addText(st.icon, { x, y: 1.0, w: 1.6, h: 0.65, fontSize: 26, align: 'center', margin: 0 });
        s.addText(st.title, { x, y: 1.65, w: 1.6, h: 0.4, fontSize: 10, bold: true, color: st.color, align: 'center', fontFace: 'Arial Black', charSpacing: 1, margin: 0 });
        s.addText(st.desc, { x, y: 2.05, w: 1.6, h: 0.7, fontSize: 10, color: C.gray, align: 'center', fontFace: 'Calibri', margin: 0 });

        // Arrow
        if (i < steps.length - 1) {
            s.addShape(pres.shapes.RECTANGLE, { x: x + 1.65, y: 2.1, w: 0.2, h: 0.04, fill: { color: C.purple }, line: { color: C.purple } });
            s.addText('▶', { x: x + 1.72, y: 1.96, w: 0.2, h: 0.3, fontSize: 10, color: C.purple, align: 'center', margin: 0 });
        }
    });

    // Tech stack row
    s.addText('TECHNOLOGY STACK', {
        x: 0.4, y: 3.55, w: 9.2, h: 0.35,
        fontSize: 12, bold: true, color: C.purple,
        fontFace: 'Arial Black', charSpacing: 2, margin: 0
    });

    const techs = [
        { name: 'Python', color: C.gold },
        { name: 'Scapy', color: C.cyan },
        { name: 'Scikit-learn', color: C.purple },
        { name: 'TensorFlow', color: 'FF8800' },
        { name: 'Flask', color: C.green },
        { name: 'Chart.js', color: C.red },
        { name: 'NSL-KDD', color: C.gold },
        { name: 'Git LFS', color: C.gray },
    ];

    techs.forEach((t, i) => {
        const x = 0.3 + i * 1.18;
        s.addShape(pres.shapes.RECTANGLE, { x, y: 4.0, w: 1.05, h: 0.45, fill: { color: C.card }, line: { color: t.color } });
        s.addText(t.name, { x, y: 4.0, w: 1.05, h: 0.45, fontSize: 9, bold: true, color: t.color, align: 'center', valign: 'middle', fontFace: 'Calibri', margin: 0 });
    });

    s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 5.58, w: 10, h: 0.04, fill: { color: C.gold }, line: { color: C.gold } });
}

// ══════════════════════════════════════════════════
// SLIDE 4 — Dataset & ML Models
// ══════════════════════════════════════════════════
{
    const s = pres.addSlide();
    s.background = { color: C.bg };

    s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.04, fill: { color: C.purple }, line: { color: C.purple } });

    s.addText('DATASET & MACHINE LEARNING', {
        x: 0.4, y: 0.15, w: 9.2, h: 0.55,
        fontSize: 22, bold: true, color: C.gold,
        fontFace: 'Arial Black', charSpacing: 3, margin: 0
    });

    // Dataset box
    s.addShape(pres.shapes.RECTANGLE, { x: 0.3, y: 0.85, w: 3.2, h: 4.3, fill: { color: C.card }, line: { color: C.cyan }, shadow: makeShadow() });
    s.addText('📊 NSL-KDD DATASET', { x: 0.3, y: 0.9, w: 3.2, h: 0.45, fontSize: 11, bold: true, color: C.cyan, align: 'center', fontFace: 'Arial Black', margin: 0 });

    const dsInfo = [
        ['Training Records', '125,973'],
        ['Test Records', '22,544'],
        ['Features', '41 per connection'],
        ['Classes', 'Normal vs Anomaly'],
        ['Format', 'ARFF (Weka)'],
        ['Split', '80% train / 20% val'],
        ['Balancing', 'SMOTE applied'],
    ];

    dsInfo.forEach(([label, val], i) => {
        const y = 1.45 + i * 0.5;
        s.addText(label + ':', { x: 0.4, y, w: 1.7, h: 0.35, fontSize: 9, color: C.gray, fontFace: 'Calibri', margin: 0 });
        s.addText(val, { x: 2.1, y, w: 1.3, h: 0.35, fontSize: 9, bold: true, color: C.white, fontFace: 'Calibri', margin: 0 });
    });

    // Models
    const models = [
        { name: 'RANDOM FOREST', acc: '99.92%', f1: '99.92%', auc: '100.00%', color: C.gold, badge: '🏆 DEPLOYED' },
        { name: 'DEEP NEURAL NET', acc: '99.51%', f1: '99.51%', auc: '99.98%', color: C.purple, badge: 'DNN' },
        { name: 'SVM', acc: '96.09%', f1: '95.99%', auc: '99.16%', color: C.cyan, badge: 'SVM' },
    ];

    models.forEach((m, i) => {
        const x = 3.8 + i * 2.05;
        s.addShape(pres.shapes.RECTANGLE, { x, y: 0.85, w: 1.85, h: 4.3, fill: { color: C.card }, line: { color: m.color }, shadow: makeShadow() });
        s.addText(m.badge, { x, y: 0.9, w: 1.85, h: 0.4, fontSize: 9, bold: true, color: m.color, align: 'center', fontFace: 'Arial Black', margin: 0 });
        s.addText(m.name, { x, y: 1.35, w: 1.85, h: 0.5, fontSize: 9, bold: true, color: C.white, align: 'center', fontFace: 'Calibri', margin: 0 });

        const metrics = [
            { label: 'Accuracy', val: m.acc },
            { label: 'F1-Score', val: m.f1 },
            { label: 'AUC-ROC', val: m.auc },
        ];

        metrics.forEach((mt, j) => {
            const y = 2.0 + j * 0.9;
            s.addShape(pres.shapes.RECTANGLE, { x: x + 0.15, y, w: 1.55, h: 0.75, fill: { color: C.darkPurp }, line: { color: C.midPurp } });
            s.addText(mt.val, { x: x + 0.15, y: y + 0.05, w: 1.55, h: 0.4, fontSize: 16, bold: true, color: m.color, align: 'center', fontFace: 'Arial Black', margin: 0 });
            s.addText(mt.label, { x: x + 0.15, y: y + 0.42, w: 1.55, h: 0.28, fontSize: 8, color: C.gray, align: 'center', fontFace: 'Calibri', margin: 0 });
        });
    });

    // Bar chart
    s.addChart(pres.charts.BAR, [{
        name: 'Accuracy %',
        labels: ['Random Forest', 'Neural Network', 'SVM'],
        values: [99.92, 99.51, 96.09]
    }], {
        x: 0.3, y: 5.0, w: 9.4, h: 0.5,
        barDir: 'bar',
        chartColors: [C.gold, C.purple, C.cyan],
        chartArea: { fill: { color: C.card } },
        catAxisLabelColor: C.gray,
        valAxisLabelColor: C.gray,
        valGridLine: { color: C.midPurp, size: 0.5 },
        catGridLine: { style: 'none' },
        showValue: true,
        dataLabelColor: C.white,
        showLegend: false,
        valAxisMinVal: 90,
        valAxisMaxVal: 100,
    });

    s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 5.58, w: 10, h: 0.04, fill: { color: C.gold }, line: { color: C.gold } });
}

// ══════════════════════════════════════════════════
// SLIDE 5 — Threat Classification
// ══════════════════════════════════════════════════
{
    const s = pres.addSlide();
    s.background = { color: C.bg };

    s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.04, fill: { color: C.purple }, line: { color: C.purple } });

    s.addText('THREAT CLASSIFICATION SYSTEM', {
        x: 0.4, y: 0.15, w: 9.2, h: 0.55,
        fontSize: 22, bold: true, color: C.gold,
        fontFace: 'Arial Black', charSpacing: 3, margin: 0
    });

    const threats = [
        { icon: '✅', label: 'NORMAL', conf: 'Prediction = 0', action: 'No action required — traffic is safe', color: C.green, bg: '001A0D' },
        { icon: '⚪', label: 'SUSPICIOUS', conf: 'Confidence < 55%', action: 'Block button shown — admin decides', color: C.gray, bg: '111118' },
        { icon: '🟡', label: 'MODERATE THREAT', conf: '55% — 75% confidence', action: 'Block button shown — admin action recommended', color: 'FFD700', bg: '1A1500' },
        { icon: '🔴', label: 'SEVERE THREAT', conf: 'Confidence > 75%', action: 'AUTOMATICALLY BLOCKED immediately!', color: C.red, bg: '1A0008' },
    ];

    threats.forEach((t, i) => {
        const y = 0.9 + i * 1.1;
        s.addShape(pres.shapes.RECTANGLE, { x: 0.3, y, w: 9.4, h: 0.95, fill: { color: t.bg }, line: { color: t.color }, shadow: makeShadow() });

        // Icon
        s.addText(t.icon, { x: 0.4, y: y + 0.1, w: 0.7, h: 0.7, fontSize: 24, align: 'center', margin: 0 });

        // Label
        s.addText(t.label, { x: 1.2, y: y + 0.08, w: 2.5, h: 0.42, fontSize: 14, bold: true, color: t.color, fontFace: 'Arial Black', margin: 0 });
        s.addText(t.conf, { x: 1.2, y: y + 0.5, w: 2.5, h: 0.35, fontSize: 10, color: C.gray, fontFace: 'Calibri', margin: 0 });

        // Arrow
        s.addText('→', { x: 3.8, y: y + 0.25, w: 0.5, h: 0.4, fontSize: 20, color: t.color, align: 'center', margin: 0 });

        // Action
        s.addText(t.action, { x: 4.4, y: y + 0.2, w: 5.1, h: 0.55, fontSize: 12, bold: i === 3, color: i === 3 ? t.color : C.white, fontFace: 'Calibri', valign: 'middle', margin: 0 });
    });

    s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 5.58, w: 10, h: 0.04, fill: { color: C.gold }, line: { color: C.gold } });
}

// ══════════════════════════════════════════════════
// SLIDE 6 — Key Features
// ══════════════════════════════════════════════════
{
    const s = pres.addSlide();
    s.background = { color: C.bg };

    s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.04, fill: { color: C.purple }, line: { color: C.purple } });

    s.addText('KEY FEATURES', {
        x: 0.4, y: 0.15, w: 9.2, h: 0.55,
        fontSize: 22, bold: true, color: C.gold,
        fontFace: 'Arial Black', charSpacing: 3, margin: 0
    });

    const features = [
        { icon: '🛡️', title: 'Real-Time Detection', desc: 'Scapy captures every packet live and classifies it instantly using ML', color: C.purple },
        { icon: '🚫', title: 'Auto-Blocking IPS', desc: 'Severe threats above 75% confidence are automatically blocked', color: C.red },
        { icon: '📊', title: 'Live Dashboard', desc: 'Real-time charts, alerts table, blocked IPs and threat statistics', color: C.cyan },
        { icon: '📡', title: 'Traffic Monitor', desc: 'Live packet feed with TCP/UDP/ICMP and service filters', color: C.green },
        { icon: '🔐', title: 'OWASP Security', desc: 'bcrypt hashing, brute force protection, rate limiting, security headers', color: C.gold },
        { icon: '📧', title: 'Email OTP System', desc: 'Forgot password via 6-digit OTP sent to registered email', color: 'FF8800' },
        { icon: '🧙', title: 'Setup Wizard', desc: 'First-time install creates personalized admin account automatically', color: C.purple },
        { icon: '📋', title: 'Historical Logs', desc: 'Persistent JSON storage with pagination, search and date filters', color: C.cyan },
        { icon: '⚔️', title: 'Attack Identification', desc: 'Identifies DoS, Port Scan, Brute Force, SYN Flood, ICMP Flood and more', color: C.gold },
        { icon: '🔑', title: 'Secure Auth', desc: 'Session management, login lockout after 5 failed attempts', color: C.green },
        { icon: '🌐', title: 'Git LFS Deploy', desc: 'Models and data hosted via Git LFS — one-click clone and run', color: C.red },
        { icon: '⚡', title: 'Auto Installer', desc: 'install.bat / install.sh registers IDS as system startup service', color: C.cyan },
    ];

    features.forEach((f, i) => {
        const col = i % 3;
        const row = Math.floor(i / 3);
        const x = 0.3 + col * 3.22;
        const y = 0.88 + row * 1.15;

        s.addShape(pres.shapes.RECTANGLE, { x, y, w: 3.0, h: 1.02, fill: { color: C.card }, line: { color: f.color }, shadow: makeShadow() });
        s.addText(f.icon, { x: x + 0.08, y: y + 0.08, w: 0.55, h: 0.55, fontSize: 20, align: 'center', margin: 0 });
        s.addText(f.title, { x: x + 0.65, y: y + 0.07, w: 2.25, h: 0.35, fontSize: 10, bold: true, color: f.color, fontFace: 'Arial Black', margin: 0 });
        s.addText(f.desc, { x: x + 0.65, y: y + 0.42, w: 2.25, h: 0.52, fontSize: 8.5, color: C.gray, fontFace: 'Calibri', margin: 0 });
    });

    s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 5.58, w: 10, h: 0.04, fill: { color: C.gold }, line: { color: C.gold } });
}

// ══════════════════════════════════════════════════
// SLIDE 7 — Dashboard Preview
// ══════════════════════════════════════════════════
{
    const s = pres.addSlide();
    s.background = { color: C.bg };

    s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.04, fill: { color: C.purple }, line: { color: C.purple } });

    s.addText('CYBERSENTINEL DASHBOARD', {
        x: 0.4, y: 0.15, w: 9.2, h: 0.55,
        fontSize: 22, bold: true, color: C.gold,
        fontFace: 'Arial Black', charSpacing: 3, margin: 0
    });

    // Mock dashboard frame
    s.addShape(pres.shapes.RECTANGLE, { x: 0.3, y: 0.85, w: 9.4, h: 4.6, fill: { color: C.card }, line: { color: C.purple }, shadow: makeShadow() });

    // Mock header bar
    s.addShape(pres.shapes.RECTANGLE, { x: 0.3, y: 0.85, w: 9.4, h: 0.55, fill: { color: C.darkPurp }, line: { color: C.purple } });
    s.addText('⚔️  CyberSentinel  |  AI-Powered Intrusion Prevention System  |  99.92%  |  12:45:30 PM', {
        x: 0.4, y: 0.88, w: 9.2, h: 0.45, fontSize: 9, color: C.gold, fontFace: 'Calibri', margin: 0
    });

    // Mock stat cards
    const mockCards = [
        { label: 'NORMAL', val: '1,247', color: C.green },
        { label: 'ATTACKS', val: '38', color: C.red },
        { label: 'SEVERE', val: '12', color: C.red },
        { label: 'MODERATE', val: '18', color: C.gold },
        { label: 'SUSPICIOUS', val: '8', color: C.gray },
        { label: 'BLOCKED', val: '12', color: C.purple },
        { label: 'TOTAL', val: '1,285', color: C.cyan },
        { label: 'ACCURACY', val: '99.92%', color: C.gold },
    ];

    mockCards.forEach((c, i) => {
        const x = 0.38 + i * 1.16;
        s.addShape(pres.shapes.RECTANGLE, { x, y: 1.5, w: 1.05, h: 0.75, fill: { color: C.bg }, line: { color: c.color } });
        s.addText(c.val, { x, y: 1.52, w: 1.05, h: 0.38, fontSize: 12, bold: true, color: c.color, align: 'center', fontFace: 'Arial Black', margin: 0 });
        s.addText(c.label, { x, y: 1.88, w: 1.05, h: 0.3, fontSize: 7, color: C.gray, align: 'center', fontFace: 'Calibri', margin: 0 });
    });

    // Mock chart area
    s.addShape(pres.shapes.RECTANGLE, { x: 0.38, y: 2.35, w: 6.0, h: 1.6, fill: { color: C.bg }, line: { color: C.midPurp } });
    s.addText('📈  Live Traffic Monitor', { x: 0.5, y: 2.38, w: 3.0, h: 0.3, fontSize: 8, color: C.purple, fontFace: 'Arial Black', margin: 0 });

    // Fake chart lines
    const linePoints = [0.3, 0.5, 0.4, 0.7, 0.6, 0.9, 0.75, 0.85, 0.95, 0.8];
    linePoints.forEach((h, i) => {
        if (i < linePoints.length - 1) {
            s.addShape(pres.shapes.RECTANGLE, {
                x: 0.5 + i * 0.52, y: 3.7 - h * 1.1,
                w: 0.52, h: 0.04,
                fill: { color: C.green }, line: { color: C.green }
            });
        }
    });

    // Mock pie
    s.addShape(pres.shapes.RECTANGLE, { x: 6.5, y: 2.35, w: 3.1, h: 1.6, fill: { color: C.bg }, line: { color: C.midPurp } });
    s.addText('🥧  Threat Breakdown', { x: 6.6, y: 2.38, w: 2.8, h: 0.3, fontSize: 8, color: C.purple, fontFace: 'Arial Black', margin: 0 });
    s.addShape(pres.shapes.OVAL, { x: 7.2, y: 2.75, w: 1.5, h: 1.1, fill: { color: C.green, transparency: 20 }, line: { color: C.green } });
    s.addShape(pres.shapes.OVAL, { x: 7.6, y: 2.95, w: 0.9, h: 0.7, fill: { color: C.red, transparency: 20 }, line: { color: C.red } });

    // Mock alerts table
    s.addShape(pres.shapes.RECTANGLE, { x: 0.38, y: 4.05, w: 9.12, h: 1.28, fill: { color: C.bg }, line: { color: C.midPurp } });
    s.addText('🚨  Recent Alerts', { x: 0.5, y: 4.07, w: 2.0, h: 0.3, fontSize: 8, color: C.purple, fontFace: 'Arial Black', margin: 0 });

    const mockAlerts = [
        { time: '12:45:28', cat: 'SEVERE THREAT', type: '💥 DoS Attack', conf: '98.5%', ip: '192.168.1.55', color: C.red },
        { time: '12:45:25', cat: 'NORMAL', type: '✅ Normal Traffic', conf: '100%', ip: '192.168.1.102', color: C.green },
        { time: '12:45:22', cat: 'MODERATE', type: '🔍 Port Scan', conf: '67.2%', ip: '192.168.1.78', color: C.gold },
    ];

    mockAlerts.forEach((a, i) => {
        const y = 4.42 + i * 0.28;
        s.addText(`${a.time}  |  ${a.type}  |  ${a.conf}  |  ${a.ip}`, {
            x: 0.5, y, w: 8.8, h: 0.24,
            fontSize: 8, color: a.color, fontFace: 'Calibri', margin: 0
        });
    });

    s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 5.58, w: 10, h: 0.04, fill: { color: C.gold }, line: { color: C.gold } });
}

// ══════════════════════════════════════════════════
// SLIDE 8 — Security & Compliance
// ══════════════════════════════════════════════════
{
    const s = pres.addSlide();
    s.background = { color: C.bg };

    s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.04, fill: { color: C.purple }, line: { color: C.purple } });

    s.addText('SECURITY & COMPLIANCE', {
        x: 0.4, y: 0.15, w: 9.2, h: 0.55,
        fontSize: 22, bold: true, color: C.gold,
        fontFace: 'Arial Black', charSpacing: 3, margin: 0
    });

    // OWASP section
    s.addShape(pres.shapes.RECTANGLE, { x: 0.3, y: 0.85, w: 4.3, h: 4.3, fill: { color: C.card }, line: { color: C.purple }, shadow: makeShadow() });
    s.addText('🛡️  OWASP TOP 10 COMPLIANCE', { x: 0.3, y: 0.9, w: 4.3, h: 0.42, fontSize: 10, bold: true, color: C.purple, align: 'center', fontFace: 'Arial Black', margin: 0 });

    const owasp = [
        { item: 'Broken Access Control', status: '✅ Protected', color: C.green },
        { item: 'Cryptographic Failures', status: '✅ bcrypt hashed', color: C.green },
        { item: 'Injection Attacks', status: '✅ No SQL used', color: C.green },
        { item: 'Insecure Design', status: '✅ Rate limited', color: C.green },
        { item: 'Auth Failures', status: '✅ 5-attempt lock', color: C.green },
        { item: 'Security Misconfiguration', status: '✅ Debug OFF', color: C.green },
        { item: 'Security Headers', status: '✅ CSP, XSS, HSTS', color: C.green },
    ];

    owasp.forEach((o, i) => {
        const y = 1.42 + i * 0.5;
        s.addText(o.item + ':', { x: 0.45, y, w: 2.1, h: 0.38, fontSize: 9, color: C.gray, fontFace: 'Calibri', margin: 0 });
        s.addText(o.status, { x: 2.55, y, w: 1.9, h: 0.38, fontSize: 9, bold: true, color: o.color, fontFace: 'Calibri', margin: 0 });
    });

    // Auth features
    s.addShape(pres.shapes.RECTANGLE, { x: 5.4, y: 0.85, w: 4.3, h: 4.3, fill: { color: C.card }, line: { color: C.gold }, shadow: makeShadow() });
    s.addText('🔐  AUTH & EMAIL SYSTEM', { x: 5.4, y: 0.9, w: 4.3, h: 0.42, fontSize: 10, bold: true, color: C.gold, align: 'center', fontFace: 'Arial Black', margin: 0 });

    const authFeatures = [
        { icon: '🧙', text: 'First-time setup wizard creates personalized admin account' },
        { icon: '🔒', text: 'Password hashed with bcrypt — never stored in plain text' },
        { icon: '🚫', text: 'Account locked after 5 failed login attempts for 5 minutes' },
        { icon: '⚡', text: 'Rate limiting — max 10 login attempts per minute' },
        { icon: '📧', text: 'Forgot password sends 6-digit OTP to registered email' },
        { icon: '⏱️', text: 'OTP expires in 5 minutes for security' },
        { icon: '📝', text: 'All security events logged with timestamp and IP address' },
    ];

    authFeatures.forEach((f, i) => {
        const y = 1.42 + i * 0.5;
        s.addText(f.icon, { x: 5.5, y, w: 0.4, h: 0.38, fontSize: 14, align: 'center', margin: 0 });
        s.addText(f.text, { x: 5.95, y, w: 3.6, h: 0.38, fontSize: 9, color: C.gray, fontFace: 'Calibri', margin: 0 });
    });

    s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 5.58, w: 10, h: 0.04, fill: { color: C.gold }, line: { color: C.gold } });
}

// ══════════════════════════════════════════════════
// SLIDE 9 — Deployment & Installation
// ══════════════════════════════════════════════════
{
    const s = pres.addSlide();
    s.background = { color: C.bg };

    s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.04, fill: { color: C.purple }, line: { color: C.purple } });

    s.addText('DEPLOYMENT & INSTALLATION', {
        x: 0.4, y: 0.15, w: 9.2, h: 0.55,
        fontSize: 22, bold: true, color: C.gold,
        fontFace: 'Arial Black', charSpacing: 3, margin: 0
    });

    // Steps
    const steps = [
        { num: '01', title: 'Clone Repository', desc: 'git clone automatically downloads all code, models and data via Git LFS', color: C.cyan },
        { num: '02', title: 'Run Installer', desc: 'install.bat (Windows) or install.sh (Linux) installs all Python packages', color: C.purple },
        { num: '03', title: 'Setup Wizard', desc: 'First launch shows setup wizard — create your admin account with email', color: C.gold },
        { num: '04', title: 'Auto Start', desc: 'IDS registers as a startup service — runs automatically on every boot', color: C.green },
        { num: '05', title: 'Open Dashboard', desc: 'Browser opens automatically at http://127.0.0.1:5000 — login and monitor', color: C.red },
    ];

    steps.forEach((st, i) => {
        const y = 0.88 + i * 0.88;
        s.addShape(pres.shapes.RECTANGLE, { x: 0.3, y, w: 9.4, h: 0.78, fill: { color: C.card }, line: { color: st.color }, shadow: makeShadow() });

        // Number circle
        s.addShape(pres.shapes.OVAL, { x: 0.38, y: y + 0.1, w: 0.55, h: 0.55, fill: { color: st.color }, line: { color: st.color } });
        s.addText(st.num, { x: 0.38, y: y + 0.1, w: 0.55, h: 0.55, fontSize: 11, bold: true, color: C.bg, align: 'center', valign: 'middle', fontFace: 'Arial Black', margin: 0 });

        s.addText(st.title, { x: 1.05, y: y + 0.08, w: 3.0, h: 0.35, fontSize: 13, bold: true, color: st.color, fontFace: 'Arial Black', margin: 0 });
        s.addText(st.desc, { x: 1.05, y: y + 0.42, w: 8.5, h: 0.3, fontSize: 10, color: C.gray, fontFace: 'Calibri', margin: 0 });
    });

    // Platform badges
    s.addShape(pres.shapes.RECTANGLE, { x: 0.3, y: 5.28, w: 9.4, h: 0.25, fill: { color: C.darkPurp }, line: { color: C.midPurp } });
    s.addText('✅ Windows   ✅ Linux   ✅ Kali Linux   ✅ Ubuntu   ✅ Any Python 3.10+ System', {
        x: 0.3, y: 5.28, w: 9.4, h: 0.25, fontSize: 9, color: C.gray, align: 'center', fontFace: 'Calibri', margin: 0
    });

    s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 5.58, w: 10, h: 0.04, fill: { color: C.gold }, line: { color: C.gold } });
}

// ══════════════════════════════════════════════════
// SLIDE 10 — Results & Testing
// ══════════════════════════════════════════════════
{
    const s = pres.addSlide();
    s.background = { color: C.bg };

    s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.04, fill: { color: C.purple }, line: { color: C.purple } });

    s.addText('RESULTS & TESTING', {
        x: 0.4, y: 0.15, w: 9.2, h: 0.55,
        fontSize: 22, bold: true, color: C.gold,
        fontFace: 'Arial Black', charSpacing: 3, margin: 0
    });

    // Big result stats
    const results = [
        { val: '99.92%', label: 'Accuracy', color: C.gold },
        { val: '99.95%', label: 'Precision', color: C.green },
        { val: '99.89%', label: 'Recall', color: C.cyan },
        { val: '100.00%', label: 'AUC-ROC', color: C.purple },
        { val: '<1%', label: 'False Positive', color: C.red },
    ];

    results.forEach((r, i) => {
        const x = 0.3 + i * 1.9;
        s.addShape(pres.shapes.RECTANGLE, { x, y: 0.85, w: 1.7, h: 1.3, fill: { color: C.card }, line: { color: r.color }, shadow: makeShadow() });
        s.addText(r.val, { x, y: 0.9, w: 1.7, h: 0.7, fontSize: 20, bold: true, color: r.color, align: 'center', fontFace: 'Arial Black', margin: 0 });
        s.addText(r.label, { x, y: 1.6, w: 1.7, h: 0.45, fontSize: 9, color: C.gray, align: 'center', fontFace: 'Calibri', margin: 0 });
    });

    // Testing section
    s.addShape(pres.shapes.RECTANGLE, { x: 0.3, y: 2.3, w: 4.3, h: 2.85, fill: { color: C.card }, line: { color: C.cyan }, shadow: makeShadow() });
    s.addText('🧪  ATTACK TESTING', { x: 0.3, y: 2.35, w: 4.3, h: 0.4, fontSize: 11, bold: true, color: C.cyan, align: 'center', fontFace: 'Arial Black', margin: 0 });

    const attacks = [
        { attack: 'SYN Flood (hping3)', result: '🔴 SEVERE — Auto-Blocked' },
        { attack: 'ICMP Ping Flood', result: '🔴 SEVERE — Auto-Blocked' },
        { attack: 'UDP Flood', result: '🟡 MODERATE — Alerted' },
        { attack: 'Port Scan (nmap)', result: '⚪ SUSPICIOUS — Flagged' },
        { attack: 'Normal Browsing', result: '✅ NORMAL — Passed' },
    ];

    attacks.forEach((a, i) => {
        const y = 2.85 + i * 0.46;
        s.addText(a.attack + ':', { x: 0.45, y, w: 2.0, h: 0.36, fontSize: 9, color: C.gray, fontFace: 'Calibri', margin: 0 });
        s.addText(a.result, { x: 2.5, y, w: 2.0, h: 0.36, fontSize: 9, bold: true, color: C.white, fontFace: 'Calibri', margin: 0 });
    });

    // Pipeline accuracy
    s.addShape(pres.shapes.RECTANGLE, { x: 5.4, y: 2.3, w: 4.3, h: 2.85, fill: { color: C.card }, line: { color: C.gold }, shadow: makeShadow() });
    s.addText('📊  PIPELINE TEST RESULTS', { x: 5.4, y: 2.35, w: 4.3, h: 0.4, fontSize: 11, bold: true, color: C.gold, align: 'center', fontFace: 'Arial Black', margin: 0 });

    const pipelineStats = [
        { label: 'Records Tested', val: '22,544' },
        { label: 'Validation Accuracy', val: '99.92%' },
        { label: 'Test Set Precision', val: '96.72%' },
        { label: 'Test AUC-ROC', val: '96.49%' },
        { label: 'Live Detection Speed', val: '< 50ms' },
    ];

    pipelineStats.forEach((p, i) => {
        const y = 2.85 + i * 0.46;
        s.addText(p.label + ':', { x: 5.55, y, w: 2.3, h: 0.36, fontSize: 9, color: C.gray, fontFace: 'Calibri', margin: 0 });
        s.addText(p.val, { x: 7.9, y, w: 1.6, h: 0.36, fontSize: 11, bold: true, color: C.gold, fontFace: 'Arial Black', margin: 0 });
    });

    s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 5.58, w: 10, h: 0.04, fill: { color: C.gold }, line: { color: C.gold } });
}

// ══════════════════════════════════════════════════
// SLIDE 11 — Where Can It Be Deployed
// ══════════════════════════════════════════════════
{
    const s = pres.addSlide();
    s.background = { color: C.bg };

    s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.04, fill: { color: C.purple }, line: { color: C.purple } });

    s.addText('WHERE CAN IT BE DEPLOYED?', {
        x: 0.4, y: 0.15, w: 9.2, h: 0.55,
        fontSize: 22, bold: true, color: C.gold,
        fontFace: 'Arial Black', charSpacing: 3, margin: 0
    });

    const deployments = [
        { icon: '🏦', title: 'Banks & Finance', desc: 'Protect banking servers from DDoS and data theft attacks', color: C.gold },
        { icon: '🏥', title: 'Hospitals', desc: 'Secure patient records and medical IoT devices on network', color: C.red },
        { icon: '🏛️', title: 'Government', desc: 'Monitor sensitive portals against foreign cyber threats', color: C.cyan },
        { icon: '🏫', title: 'Universities', desc: 'Protect campus networks and thousands of student records', color: C.purple },
        { icon: '📡', title: 'Telecom', desc: 'Monitor large network infrastructure for botnet traffic', color: C.green },
        { icon: '🌐', title: 'IoT Networks', desc: 'Gateway monitoring for smart homes and smart factories', color: 'FF8800' },
        { icon: '🏭', title: 'SMEs', desc: 'Enterprise-level AI security at zero licensing cost', color: C.gold },
        { icon: '🔬', title: 'Research Labs', desc: 'Academic cybersecurity research and experimentation', color: C.cyan },
    ];

    deployments.forEach((d, i) => {
        const col = i % 4;
        const row = Math.floor(i / 4);
        const x = 0.3 + col * 2.38;
        const y = 0.9 + row * 2.1;

        s.addShape(pres.shapes.RECTANGLE, { x, y, w: 2.2, h: 1.85, fill: { color: C.card }, line: { color: d.color }, shadow: makeShadow() });
        s.addText(d.icon, { x, y: y + 0.12, w: 2.2, h: 0.65, fontSize: 28, align: 'center', margin: 0 });
        s.addText(d.title, { x, y: y + 0.78, w: 2.2, h: 0.38, fontSize: 11, bold: true, color: d.color, align: 'center', fontFace: 'Arial Black', margin: 0 });
        s.addText(d.desc, { x, y: y + 1.15, w: 2.2, h: 0.6, fontSize: 8.5, color: C.gray, align: 'center', fontFace: 'Calibri', margin: 0 });
    });

    s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 5.58, w: 10, h: 0.04, fill: { color: C.gold }, line: { color: C.gold } });
}

// ══════════════════════════════════════════════════
// SLIDE 12 — Future Work
// ══════════════════════════════════════════════════
{
    const s = pres.addSlide();
    s.background = { color: C.bg };

    s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.04, fill: { color: C.purple }, line: { color: C.purple } });

    s.addText('FUTURE ENHANCEMENTS', {
        x: 0.4, y: 0.15, w: 9.2, h: 0.55,
        fontSize: 22, bold: true, color: C.gold,
        fontFace: 'Arial Black', charSpacing: 3, margin: 0
    });

    const future = [
        { icon: '🌍', title: 'GeoIP Location', desc: 'Show which country each attack originates from on a live world map', color: C.cyan, phase: 'Phase 2' },
        { icon: '📤', title: 'PDF Report Export', desc: 'One-click generate and download security reports as PDF files', color: C.gold, phase: 'Phase 2' },
        { icon: '📱', title: 'Mobile Responsive', desc: 'Full dashboard access from mobile phones and tablets', color: C.purple, phase: 'Phase 2' },
        { icon: '🔔', title: 'Email Alerts', desc: 'Send instant email notification when severe attack is detected', color: C.red, phase: 'Phase 2' },
        { icon: '☁️', title: 'Cloud Deployment', desc: 'Deploy on Railway.app with permanent HTTPS URL accessible anywhere', color: C.green, phase: 'Phase 3' },
        { icon: '🔥', title: 'Real Firewall', desc: 'Integrate with Windows Firewall and iptables for true IP blocking', color: 'FF8800', phase: 'Phase 3' },
        { icon: '🧠', title: 'Federated Learning', desc: 'Train model on distributed network data without sharing raw packets', color: C.cyan, phase: 'Phase 4' },
        { icon: '📊', title: 'SIEM Integration', desc: 'Connect with enterprise SIEM platforms via REST API', color: C.gold, phase: 'Phase 4' },
    ];

    future.forEach((f, i) => {
        const col = i % 2;
        const row = Math.floor(i / 2);
        const x = 0.3 + col * 4.85;
        const y = 0.9 + row * 1.12;

        s.addShape(pres.shapes.RECTANGLE, { x, y, w: 4.6, h: 0.95, fill: { color: C.card }, line: { color: f.color }, shadow: makeShadow() });

        // Phase badge
        s.addShape(pres.shapes.RECTANGLE, { x: x + 3.5, y: y + 0.08, w: 0.95, h: 0.3, fill: { color: f.color }, line: { color: f.color } });
        s.addText(f.phase, { x: x + 3.5, y: y + 0.08, w: 0.95, h: 0.3, fontSize: 7, bold: true, color: C.bg, align: 'center', valign: 'middle', fontFace: 'Arial Black', margin: 0 });

        s.addText(f.icon, { x: x + 0.08, y: y + 0.1, w: 0.55, h: 0.6, fontSize: 20, align: 'center', margin: 0 });
        s.addText(f.title, { x: x + 0.7, y: y + 0.08, w: 2.7, h: 0.35, fontSize: 11, bold: true, color: f.color, fontFace: 'Arial Black', margin: 0 });
        s.addText(f.desc, { x: x + 0.7, y: y + 0.44, w: 3.8, h: 0.42, fontSize: 9, color: C.gray, fontFace: 'Calibri', margin: 0 });
    });

    s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 5.58, w: 10, h: 0.04, fill: { color: C.gold }, line: { color: C.gold } });
}

// ══════════════════════════════════════════════════
// SLIDE 13 — Thank You
// ══════════════════════════════════════════════════
{
    const s = pres.addSlide();
    s.background = { color: C.bg };

    // Glow effects
    s.addShape(pres.shapes.OVAL, { x: -2, y: -2, w: 8, h: 8, fill: { color: C.purple, transparency: 90 }, line: { color: C.purple, transparency: 90 } });
    s.addShape(pres.shapes.OVAL, { x: 5, y: 1, w: 6, h: 6, fill: { color: C.gold, transparency: 93 }, line: { color: C.gold, transparency: 93 } });

    s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0, w: 10, h: 0.04, fill: { color: C.purple }, line: { color: C.purple } });
    s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 0.04, w: 10, h: 0.04, fill: { color: C.gold }, line: { color: C.gold } });

    s.addText('⚔️', { x: 4.3, y: 0.7, w: 1.4, h: 1.0, fontSize: 48, align: 'center' });

    s.addText('THANK YOU', {
        x: 0.5, y: 1.65, w: 9, h: 1.0,
        fontSize: 56, bold: true, color: C.gold,
        align: 'center', fontFace: 'Arial Black', charSpacing: 8, margin: 0
    });

    s.addText('CyberSentinel — Protecting Networks with Artificial Intelligence', {
        x: 0.5, y: 2.7, w: 9, h: 0.45,
        fontSize: 14, color: C.gray, align: 'center', fontFace: 'Calibri', margin: 0
    });

    s.addShape(pres.shapes.RECTANGLE, { x: 3.0, y: 3.25, w: 4.0, h: 0.03, fill: { color: C.purple }, line: { color: C.purple } });

    // Final stats row
    const finalStats = [
        { val: '99.92%', label: 'Accuracy' },
        { val: '3 Models', label: 'Trained' },
        { val: '4 Tiers', label: 'Threat Levels' },
        { val: '12+', label: 'Features' },
    ];

    finalStats.forEach((st, i) => {
        const x = 1.0 + i * 2.2;
        s.addText(st.val, { x, y: 3.5, w: 2.0, h: 0.55, fontSize: 20, bold: true, color: C.purple, align: 'center', fontFace: 'Arial Black', margin: 0 });
        s.addText(st.label, { x, y: 4.05, w: 2.0, h: 0.35, fontSize: 10, color: C.gray, align: 'center', fontFace: 'Calibri', margin: 0 });
    });

    s.addText('Questions & Discussion', {
        x: 0.5, y: 4.55, w: 9, h: 0.4,
        fontSize: 16, color: C.gold, align: 'center',
        fontFace: 'Calibri', italic: true, margin: 0
    });

    s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 5.2, w: 10, h: 0.04, fill: { color: C.purple }, line: { color: C.purple } });
    s.addText('BS Cybersecurity  |  Final Year Project 2025-2026  |  Sir Syed CASE Institute of Technology', {
        x: 0, y: 5.28, w: 10, h: 0.28, fontSize: 9, color: C.gray, align: 'center', fontFace: 'Calibri', margin: 0
    });
    s.addShape(pres.shapes.RECTANGLE, { x: 0, y: 5.58, w: 10, h: 0.04, fill: { color: C.gold }, line: { color: C.gold } });
}

// ─── Save ─────────────────────────────────────────
pres.writeFile({ fileName: '/mnt/user-data/outputs/CyberSentinel_Presentation.pptx' })
    .then(() => console.log('✅ Presentation created!'))
    .catch(e => console.error('❌ Error:', e));