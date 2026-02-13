# 🎨 Lovable Prompt for SentinelOps Frontend

Copy and paste this entire prompt into Lovable to generate your frontend!

---

## 🚀 Project Brief

Create a **stunning, modern dashboard** for **SentinelOps** - an autonomous AI-powered Site Reliability Engineer that monitors Kubernetes clusters, auto-scales based on load, auto-heals crashed pods, and optimizes infrastructure costs in real-time.

---

## 🎨 Design Theme: **"Glassmorphic Cyberpunk"**

### Visual Style
- **Glassmorphism effects** with frosted glass cards, backdrop blur, and transparency
- **Vibrant gradient backgrounds** - Purple/pink/blue cosmic gradients (think: Aurora Borealis in space)
- **Neon accents** - Glowing borders, hover effects, subtle animations
- **Floating elements** - Cards that appear to float above the background
- **Smooth micro-animations** - Elements fade in, slide up, pulse gently
- **Modern typography** - Inter or Poppins font, bold numbers, lightweight labels
- **3D depth** - Layered shadows, elevation effects

### Color Palette
```
Primary Background: Linear gradient from #6366f1 (indigo) → #8b5cf6 (purple) → #ec4899 (pink)
Card Background: rgba(255, 255, 255, 0.1) with backdrop-blur-lg
Card Borders: rgba(255, 255, 255, 0.2)
Text Primary: #ffffff
Text Secondary: rgba(255, 255, 255, 0.7)
Accent Success: #10b981 (emerald)
Accent Warning: #f59e0b (amber)
Accent Danger: #ef4444 (red)
Accent Info: #06b6d4 (cyan)
Glow/Neon: #a855f7 (purple glow for important elements)
```

### Key Visual Elements
- Animated gradient background that slowly shifts
- Glassmorphic cards with slight blur and transparency
- Neon glow effects on hover
- Subtle particle effects or grid overlay in background
- Smooth spring animations for all transitions
- Floating action buttons with ripple effects
- Real-time data updates with smooth number transitions
- Progress bars with gradient fills and glow

---

## 📱 Layout & Components

### 1. Header (Top Bar)
```
┌─────────────────────────────────────────────────────────┐
│ 🛡️ SentinelOps     [Real-time Stats]    🟢 Connected  │
└─────────────────────────────────────────────────────────┘
```
- Logo on left with subtle glow
- Animated connection status pill (pulsing green dot)
- Last updated timestamp with fade animation

### 2. Hero Metrics Section (Top)
**4 Large Glassmorphic Cards in a Grid**

```
┌──────────────┬──────────────┬──────────────┬──────────────┐
│   💻 CPU     │   🧠 MEMORY  │   📦 PODS    │   💰 COST    │
│              │              │              │              │
│    45.2%     │    62.8%     │      5       │   $2.88/day  │
│   ━━━━━      │   ━━━━━━━━   │   Healthy    │   ↓ $1.25    │
│   Normal     │   Moderate   │              │   saved      │
└──────────────┴──────────────┴──────────────┴──────────────┘
```

**Each Card Should Have:**
- Icon at top (animated on hover - slight bounce)
- Large number with gradient text
- Visual indicator (progress bar with gradient or ring chart)
- Small status label below
- Smooth color transitions based on value (green=good, yellow=warning, red=critical)
- Hover effect: lift up, increase glow
- Numbers should animate when they change (counting animation)

### 3. Main Content (Two Columns on Desktop)

**Left Column (60% width):**

**A. Live Metrics Chart (Glassmorphic Card)**
```
┌─────────────────────────────────────────┐
│  📊 System Performance (Last Hour)      │
│                                         │
│  [Smooth animated line chart]          │
│  - CPU usage (cyan line)               │
│  - Memory usage (purple line)          │
│  - Pod count (pink line)               │
│                                         │
│  Interactive: Hover shows exact values  │
└─────────────────────────────────────────┘
```
- Use Chart.js or Recharts
- Gradient fills under lines
- Smooth animations
- Glowing data points
- Tooltip with glassmorphic design

**B. Cost Analysis (Glassmorphic Card)**
```
┌─────────────────────────────────────────┐
│  💰 Cost Optimization                   │
│                                         │
│  Current Daily Cost: $2.88             │
│  Monthly Projection: $86.40            │
│                                         │
│  💚 Saved Today: $1.25                  │
│  📊 Monthly Savings: $37.50            │
│                                         │
│  [Animated savings badge with glow]     │
│  "You're saving 43% vs baseline!"      │
└─────────────────────────────────────────┘
```
- Animated progress/savings bar
- Celebrate savings with confetti animation
- Pulsing badge for high savings

**Right Column (40% width):**

**C. Live Incident Feed (Scrollable)**
```
┌─────────────────────────────────────────┐
│  🔄 Autonomous Actions (Live)           │
│                                         │
│  🟢 15:42:18 • CPU Overload            │
│  ↳ Scaled nginx-demo: 3 → 5 pods      │
│  ✓ Resolved in 8.2s                    │
│                                         │
│  🔵 14:30:10 • Pod Crash Detected      │
│  ↳ Restarted pod nginx-demo-abc12     │
│  ✓ Resolved in 12.5s                   │
│                                         │
│  🟡 13:15:05 • Memory Warning          │
│  ↳ Scaled up +1 pod                    │
│  ✓ Resolved in 6.1s                    │
│                                         │
│  [View All Incidents →]                │
└─────────────────────────────────────────┘
```
- Each incident is a mini glassmorphic card
- Color-coded left border (green=resolved, orange=warning, red=error)
- Fade-in animation when new incidents appear
- Timeline connector dots
- Hover: expand to show more details
- Auto-scroll to show latest

**D. Optimization Recommendations**
```
┌─────────────────────────────────────────┐
│  💡 Smart Recommendations               │
│                                         │
│  ⚠️ Reduce baseline replica count       │
│     Potential savings: $15-30/month    │
│     [Confidence: HIGH]                  │
│     [Apply Suggestion →]                │
│                                         │
│  ✨ System is well-optimized           │
│     No immediate actions needed         │
│                                         │
└─────────────────────────────────────────┘
```
- Each recommendation in a nested glass card
- Severity badge with glow
- Action button with hover effect
- Celebrate when "well-optimized"

### 4. Chaos Testing Control Panel (Bottom)
```
┌─────────────────────────────────────────────────────────┐
│  🔥 CHAOS ENGINEERING LAB                               │
│                                                         │
│  [⚡ Trigger CPU Spike]  [💥 Crash Pod]  [🌊 Cascade]  │
│                                                         │
│  Test the autonomous healing capabilities               │
└─────────────────────────────────────────────────────────┘
```
- Danger zone styling (red/orange glow)
- Buttons with pulsing animation
- Confirmation modal before triggering (glassmorphic)
- Show active simulation status with countdown timer

### 5. Footer (Subtle)
```
Built with ❤️ by SentinelOps • Last refresh: 2s ago • API Status: 🟢
```

---

## 🎯 Technical Requirements

### API Integration

**Base URL:** `http://127.0.0.1:8000`

**Main Endpoint (Use this for everything):**
```javascript
// Fetch all data in one call
const response = await fetch('http://127.0.0.1:8000/dashboard/stats?hours=24');
const data = await response.json();

// Response structure:
{
  cluster: {
    total_pods: 5,
    healthy_pods: 5,
    unhealthy_pods: 0
  },
  metrics: {
    cpu_usage: 45.2,      // percentage
    memory_usage: 62.8,   // percentage
    pod_count: 5
  },
  cost: {
    hourly: 0.12,
    daily: 2.88,
    monthly: 86.40
  },
  savings: {
    total_saved: 1.25,
    projected_monthly: 37.50,
    scale_down_count: 3,
    scale_up_count: 2
  },
  incidents: {
    total: 15,
    successful: 14,
    success_rate: 93.3,
    recent: [...]  // Array of incident objects
  },
  recommendations: [...],  // Array of recommendation objects
  health: {
    status: "healthy",
    kubernetes: "connected",
    prometheus: "connected"
  }
}
```

**Real-time Updates:**
```javascript
// Poll every 5 seconds for live feel
setInterval(async () => {
  const response = await fetch('http://127.0.0.1:8000/stats/summary');
  const data = await response.json();
  // Update metrics with smooth transitions
}, 5000);
```

**Chaos Testing:**
```javascript
// Trigger CPU spike
await fetch('http://127.0.0.1:8000/simulate/cpu_spike?duration=120', {
  method: 'POST'
});

// Crash a pod
await fetch('http://127.0.0.1:8000/simulate/crash', {
  method: 'POST'
});
```

### Responsive Design
- **Desktop (1200px+):** Two-column layout as shown above
- **Tablet (768-1199px):** Stack columns, full-width cards
- **Mobile (<768px):** Single column, compact cards, bottom navigation

### Animations & Interactions
1. **Page Load:**
   - Stagger fade-in animation for cards (0.1s delay between each)
   - Gradient background animated loop (slow, subtle)
   - Numbers count up from 0 to current value

2. **Data Updates:**
   - Smooth number transitions (spring animation)
   - Flash effect on change (brief glow)
   - Chart data animates smoothly

3. **Hover Effects:**
   - Cards: Lift up 4px, increase glow
   - Buttons: Scale 1.05, increase glow
   - Charts: Highlight hovered series

4. **Loading States:**
   - Skeleton loaders with shimmer effect
   - Pulse animation on refresh
   - Spinner with glassmorphic background

5. **Success Celebrations:**
   - Confetti when "well-optimized"
   - Checkmark animation when incidents resolve
   - Subtle particle burst on successful actions

### Error Handling
- Glassmorphic error modal if API fails
- Retry button with countdown
- Fallback to cached data with warning indicator

---

## 🎨 Component-Specific Details

### Metric Cards (Top 4 Cards)
```jsx
- Height: 160px
- Glassmorphic: backdrop-blur-xl, bg-white/10
- Border: 1px solid white/20
- Shadow: 0 8px 32px rgba(0,0,0,0.12)
- Hover: translateY(-4px), increase shadow
- Icon: 48px, subtle float animation
- Number: 56px font, gradient text
- Progress bar: Gradient fill, rounded, glowing
- Status label: 12px, uppercase, semi-transparent
```

### Chart Card
```jsx
- Use Chart.js with glassmorphic customization
- Grid lines: semi-transparent white
- Lines: 3px width, gradient stroke
- Fill: gradient with low opacity
- Points: Glow effect on hover
- Tooltip: Glassmorphic card
- Legend: Icons + text, toggleable
```

### Incident Timeline
```jsx
- Each item: Mini glass card
- Timeline dots: Connected with gradient line
- Color coding: Border-left 3px width
- Timestamp: Small, monospace font
- Action: Medium weight, white
- Result: Success icon + timing
- Hover: Expand 4px, show more details
- New items: Slide in from top
```

### Chaos Buttons
```jsx
- Large: 48px height
- Red/orange gradient background
- White text with medium weight
- Border: Glowing animation (pulse)
- Icon: Lightning, explosion, wave
- Hover: Scale 1.05, stronger glow
- Active state: Scale 0.95
- Loading: Spinner inside button
```

### Modals/Dialogs
```jsx
- Overlay: backdrop-blur-sm, bg-black/30
- Modal: Large glassmorphic card
- Border: Glowing gradient
- Buttons: Primary (glow) + Secondary (outline)
- Animation: Scale in from center
```

---

## 🚀 User Experience Flow

### Initial Load
1. Show animated gradient background immediately
2. Fade in header with "Connecting..." status
3. Stagger fade-in all cards with skeleton loaders
4. Once data loads, animate numbers counting up
5. Change status to "Connected" with celebration effect

### Real-time Updates
1. Subtle flash on metric cards when values change
2. New incidents fade in at top of timeline
3. Chart data smoothly transitions
4. Cost savings badge pulses if savings increase

### Chaos Testing Demo
1. User clicks "Trigger CPU Spike"
2. Confirmation modal appears (glassmorphic)
3. After confirm, button shows loading spinner
4. Success toast notification appears
5. CPU metric starts rising (animated)
6. Watch incident feed show detection
7. See auto-scaling action in real-time
8. Celebrate when resolved with checkmark animation

---

## 🎬 Special Features

### Easter Eggs
- Click logo 5 times: Matrix rain effect on background
- Konami code: Toggle between color themes
- Double-tap metrics: Full-screen chart mode

### Accessibility
- ARIA labels on all interactive elements
- Keyboard navigation support
- High contrast option for metrics
- Reduced motion mode respects user preferences

### Performance
- Lazy load chart library
- Debounce API calls
- Cache data with 5s stale-while-revalidate
- Optimize animations for 60fps
- Use CSS transforms (not positioning) for smooth animation

---

## 📋 Component Checklist

### Must-Have Components:
- [ ] Animated gradient background
- [ ] Glassmorphic header with connection status
- [ ] 4 Hero metric cards (CPU, Memory, Pods, Cost)
- [ ] Live performance chart (line/area chart)
- [ ] Cost analysis card with savings
- [ ] Incident timeline feed (scrollable)
- [ ] Recommendations panel
- [ ] Chaos testing control panel
- [ ] Loading states (skeletons)
- [ ] Error handling (modals)
- [ ] Toast notifications
- [ ] Smooth animations throughout

### Optional But Awesome:
- [ ] Particle effects in background
- [ ] Confetti on milestones
- [ ] Sound effects (subtle, toggleable)
- [ ] Dark/light theme toggle
- [ ] Export data button
- [ ] Share dashboard link
- [ ] Settings panel

---

## 🎨 CSS Framework & Libraries

**Recommended Stack:**
- **React** (with hooks)
- **Tailwind CSS** (for glassmorphism utilities)
- **Framer Motion** (for smooth animations)
- **Chart.js** or **Recharts** (for charts)
- **React Hot Toast** (for notifications)
- **Lucide React** (for icons)

**Key Tailwind Classes to Use:**
```css
backdrop-blur-xl
bg-white/10
border-white/20
shadow-2xl
hover:transform
transition-all
duration-300
ease-in-out
```

---

## 🎯 Success Criteria

Your frontend is awesome if:
- ✅ Loads in under 2 seconds
- ✅ Animations are smooth (60fps)
- ✅ Works on mobile, tablet, and desktop
- ✅ Data updates in real-time (polls every 5s)
- ✅ Chaos testing works with visual feedback
- ✅ Looks modern, premium, and different from typical dashboards
- ✅ People say "WOW!" when they first see it

---

## 🚀 Build This!

This is a **production-ready SaaS dashboard** that will blow people away. The glassmorphic cyberpunk theme is trendy, modern, and stands out from boring enterprise dashboards.

**Remember:**
- Every element should feel premium
- Animations should be smooth, not janky
- Data should update seamlessly
- The whole experience should feel alive and intelligent

**Go make it SEXY! 🎨✨**
