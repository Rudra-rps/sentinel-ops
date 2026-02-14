
# 🏟️ SentinelOps — Stadium Scoreboard Dashboard

A fully-featured infrastructure monitoring dashboard reskinned as a **live stadium scoreboard experience** — dark arena backgrounds, LED-style numbers, score tickers, and the energy of a packed sports venue.

---

## 🎨 Design Theme: "Stadium Scoreboard"

- **Dark arena background** with deep navy/black and subtle stadium light glow effects
- **LED-style numbers** (monospace, bright, glowing) for all metrics — like a real scoreboard
- **Scoreboard-style cards** with dark metallic frames, neon borders, and pixel-grid textures
- **Team color accents**: Emerald green (healthy/success), Amber gold (warnings), Red (critical/danger), Cyan (info)
- **Stadium ambiance**: Subtle spotlight effects, gradient glows simulating arena lighting
- **Glassmorphic overlays** on top of the dark theme for depth
- **Animated gradient** background simulating slow-moving stadium lights

---

## 📱 Pages & Components

### 1. Header — "Jumbotron Bar"
- SentinelOps logo with stadium glow effect
- Live connection status as a pulsing LED indicator (🟢 Connected)
- "LIVE" badge with blinking animation (like a broadcast indicator)
- Quick stats ticker scrolling across the top (like a sports news ticker)

### 2. Hero Metrics — "The Scoreboard"
Four large scoreboard-style cards in a grid:
- **💻 CPU Usage** — LED percentage display with progress bar
- **🧠 Memory Usage** — LED percentage with color-coded status
- **📦 Active Pods** — Large LED number with healthy/unhealthy count
- **💰 Cost/Day** — Dollar amount with savings indicator

Each card features:
- LED-style animated counting numbers
- Scoreboard frame styling (dark metallic with neon borders)
- Color transitions based on status (green → yellow → red)
- Hover: lift up with increased glow

### 3. Performance Chart — "Game Stats"
- Live line/area chart showing CPU, Memory, and Pod count over time
- Styled like a sports broadcast stat overlay
- Gradient fills under lines, glowing data points
- Scoreboard-styled tooltip on hover
- Uses Recharts (already installed)

### 4. Cost Analysis — "Season Stats"
- Current daily cost displayed as a big LED number
- Monthly projection
- Savings displayed like "points scored" with celebration effects
- Animated savings progress bar with gradient fill
- "You're saving 43% vs baseline!" displayed like a highlight stat

### 5. Incident Feed — "Play-by-Play"
- Scrollable timeline of autonomous actions
- Each incident styled as a mini scoreboard card
- Color-coded left borders (green = resolved, amber = warning, red = error)
- Timestamps in monospace LED font
- New incidents slide in from the top with animation
- Timeline connector dots like a game timeline

### 6. Recommendations — "Coach's Corner"
- Smart optimization suggestions in nested scoreboard cards
- Severity badges with glow effects
- "Apply Suggestion" action buttons
- Celebration state when system is well-optimized

### 7. Chaos Testing Panel — "Overtime Mode"
- Styled as a danger zone with red/orange arena glow
- Three action buttons: ⚡ CPU Spike, 💥 Crash Pod, 🌊 Cascade Failure
- Pulsing neon button animations
- Confirmation modal (glassmorphic with scoreboard styling)
- Active simulation status with countdown timer
- Visual feedback showing the chaos test in progress

### 8. Footer — "Broadcast Bar"
- Subtle bar with last refresh time, API status indicator
- Styled like a sports broadcast lower third

---

## ✨ Animations & Interactions

- **Page load**: Staggered fade-in of all cards, numbers count up from 0
- **Data updates**: LED numbers smoothly transition, brief flash/glow on change
- **Hover effects**: Cards lift with increased shadow and neon glow
- **Loading states**: Skeleton loaders with shimmer effect
- **Toast notifications**: Scoreboard-styled success/error toasts using Sonner
- **Easter eggs**: Click logo 5x for matrix rain effect, Konami code for theme toggle

---

## 📊 Data

All data will be **realistic mock data** — no API calls needed. The dashboard will simulate:
- Live-updating metrics (CPU, Memory, Pods, Cost) cycling through realistic values
- A history of incidents with timestamps and resolution details
- Cost savings calculations
- Optimization recommendations
- Simulated chaos test responses with visual feedback

---

## 📐 Responsive Design

- **Desktop (1200px+)**: Two-column layout — chart + cost on left, incidents + recommendations on right
- **Tablet (768-1199px)**: Stacked single column, full-width cards
- **Mobile (<768px)**: Compact scoreboard cards, scrollable sections
