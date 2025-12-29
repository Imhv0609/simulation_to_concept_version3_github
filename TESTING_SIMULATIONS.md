# Testing New Simulations with URL Parameters

## 🎯 Quick Test Links

With the HTTP server running on port 8001, you can test the new simulations:

### 1. **Earth's Rotation & Revolution** 🌍

#### Test Different Axial Tilts:
```
http://localhost:8001/rotAndRev.html?rotationSpeed=50&axialTilt=0&revolutionSpeed=50
```
*No tilt = No seasons*

```
http://localhost:8001/rotAndRev.html?rotationSpeed=50&axialTilt=23.5&revolutionSpeed=50
```
*Earth's actual tilt*

```
http://localhost:8001/rotAndRev.html?rotationSpeed=50&axialTilt=30&revolutionSpeed=50
```
*Extreme tilt = Extreme seasons*

#### Test Different Speeds:
```
http://localhost:8001/rotAndRev.html?rotationSpeed=100&axialTilt=23.5&revolutionSpeed=100
```
*Fast rotation and revolution*

```
http://localhost:8001/rotAndRev.html?rotationSpeed=10&axialTilt=23.5&revolutionSpeed=10
```
*Slow rotation and revolution*

---

### 2. **Light & Shadows** 💡

#### Test Different Light Distances:
```
http://localhost:8001/lightsShadows.html?lightDistance=1&objectType=Opaque&objectSize=5
```
*Close light = Large shadow*

```
http://localhost:8001/lightsShadows.html?lightDistance=10&objectType=Opaque&objectSize=5
```
*Far light = Small shadow*

#### Test Different Object Types:
```
http://localhost:8001/lightsShadows.html?lightDistance=5&objectType=Opaque&objectSize=5
```
*Opaque = Dark, clear shadow*

```
http://localhost:8001/lightsShadows.html?lightDistance=5&objectType=Translucent&objectSize=5
```
*Translucent = Lighter, fuzzy shadow*

```
http://localhost:8001/lightsShadows.html?lightDistance=5&objectType=Transparent&objectSize=5
```
*Transparent = No shadow*

#### Test Different Object Sizes:
```
http://localhost:8001/lightsShadows.html?lightDistance=5&objectType=Opaque&objectSize=1
```
*Small object = Small shadow*

```
http://localhost:8001/lightsShadows.html?lightDistance=5&objectType=Opaque&objectSize=10
```
*Large object = Large shadow*

---

### 3. **Simple Pendulum** ⏰

```
http://localhost:8001/simple_pendulum.html?length=1&oscillations=20&autoStart=true
```
*Short pendulum = Fast swings*

```
http://localhost:8001/simple_pendulum.html?length=10&oscillations=20&autoStart=true
```
*Long pendulum = Slow swings*

---

## 🧪 How URL Parameters Work

### Earth's Rotation & Revolution
```javascript
// In rotAndRev.html
const urlParams = new URLSearchParams(window.location.search);
const rotationValue = urlParams.get('rotationSpeed');  // 0-100
const tiltValue = urlParams.get('axialTilt');          // 0-30
const revolutionValue = urlParams.get('revolutionSpeed'); // 0-100
```

### Light & Shadows
```javascript
// In lightsShadows.html
const urlParams = new URLSearchParams(window.location.search);
const lightDistanceValue = urlParams.get('lightDistance'); // 1-10
const objectTypeValue = urlParams.get('objectType');       // Opaque/Translucent/Transparent
const objectSizeValue = urlParams.get('objectSize');       // 1-10
```

### Simple Pendulum
```javascript
// In simple_pendulum.html
const urlParams = new URLSearchParams(window.location.search);
const lengthValue = urlParams.get('length');               // 1-10
const oscValue = urlParams.get('oscillations');            // 5-50
const autoStart = urlParams.get('autoStart');              // true/false
```

---

## 📊 Parameter Ranges

### Earth's Rotation & Revolution
| Parameter | Range | Effect |
|-----------|-------|--------|
| `rotationSpeed` | 0-100% | Day/night cycle speed |
| `axialTilt` | 0-30° | Season intensity |
| `revolutionSpeed` | 0-100% | Year length |

### Light & Shadows
| Parameter | Range | Effect |
|-----------|-------|--------|
| `lightDistance` | 1-10 units | Shadow size (closer = larger) |
| `objectType` | Opaque/Translucent/Transparent | Shadow darkness |
| `objectSize` | 1-10 units | Shadow size |

### Simple Pendulum
| Parameter | Range | Effect |
|-----------|-------|--------|
| `length` | 1-10 units | Swing speed (longer = slower) |
| `oscillations` | 5-50 count | Total time |
| `autoStart` | true/false | Auto-click start button |

---

## ✅ Verification Checklist

- [ ] **rotAndRev.html** - Try changing axial tilt from 0 to 30
- [ ] **rotAndRev.html** - Try changing rotation speed to see faster/slower day cycle
- [ ] **lightsShadows.html** - Try moving light from distance 1 to 10 (shadow shrinks)
- [ ] **lightsShadows.html** - Try switching object types (Opaque → Translucent → Transparent)
- [ ] **simple_pendulum.html** - Verify autoStart works with URL parameter

---

## 🎓 Teaching Integration

These URL parameters allow the teaching agent to:
1. **Control simulations programmatically** via URL
2. **Guide students** through parameter explorations
3. **Demonstrate cause-and-effect** relationships
4. **Auto-start simulations** to reduce friction

Example teacher flow:
```
Teacher: "Let me change the axial tilt to 0 degrees. OBSERVE: What happens to the seasons?"
→ System opens: rotAndRev.html?axialTilt=0&rotationSpeed=50&revolutionSpeed=50

Student: "There are no seasons anymore!"
→ ✅ Correct understanding detected!

Teacher: "Excellent! Now let's increase it to 30 degrees..."
→ System opens: rotAndRev.html?axialTilt=30&rotationSpeed=50&revolutionSpeed=50
```

---

## 🚀 Start Testing

```bash
# Start HTTP server (if not already running)
cd simulations
python3 -m http.server 8001

# Open in browser:
# http://localhost:8001/rotAndRev.html?rotationSpeed=70&axialTilt=15&revolutionSpeed=50
```

---

**All three simulations now support URL parameters! 🎉**
