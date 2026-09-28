# Smart Traffic Light Intersection (Python + Pygame)

## التشغيل
    pip install -r requirements.txt
    python main.py

## التحكم
| مفتاح | وظيفته |
|---|---|
| F / S | Fixed Mode / Smart Mode (التبديل أثناء التشغيل بدون قفزة في الإشارة) |
| SPACE | إيقاف مؤقت / استئناف |
| R | Reset (يطبع نتائج المحاكاة في الـConsole) |
| 1-4 | LOW / MEDIUM / HIGH / VERY_HIGH |
| T | تبديل وضع الوقت: AUTO / NIGHT / NORMAL / AM RUSH / PM RUSH |
| E | إطلاق مركبة طوارئ (إسعاف / إطفاء / شرطة) |
| C | مقارنة Fixed vs Smart (محاكاة headless فعلية بنفس الـseed) |

كل شيء أيضاً متاح كأزرار في اللوحة الجانبية (START/PAUSE/RESET، الكثافة، السرعة 0.5x-10x).

## كيف يعمل
- **السيارات**: تسارع/فرملة/مسافة أمان؛ لا تداخل ولا عبور للأحمر. عند الأصفر تتوقف السيارة إن استطاعت
  التوقف بأمان (v²/2a <= المسافة) وإلا تكمل.
- **الإشارات**: GREEN -> YELLOW -> ALL_RED -> الاتجاه الآخر (لا انتقال مباشر).
- **Fixed**: أخضر ثابت 30 ثانية.
- **Smart**: `Green = 15 + 2*cars + 0.2*avg_wait` ثم clamp بين MIN_GREEN و MAX_GREEN.
  Traffic Score = `cars + 1.5*queue + 0.2*avg_wait`. الأخضر ينتهي مبكراً إذا الطريق فارغ (بعد MIN_SAFE_GREEN)،
  ويبقى إذا لم ينتظر أحد في الاتجاه الآخر، ويُجبر على التبديل عند MAX_GREEN أو عند
  وصول انتظار أي سيارة إلى MAX_WAITING_TIME (Starvation guard).
- **الطوارئ**: اكتشاف الاتجاه -> إنهاء الأخضر المعارض بأمان -> أخضر للمركبة -> عودة للتحكم العادي.
- **الازدحام خارج الخريطة**: السيارات التي لا تجد مكاناً للدخول تُحتسب في backlog وتُحسب في الـscore.

## الهيكل
    config.py                 كل الثوابت (التوقيتات، الكثافة، الأوزان)
    simulation/               car, traffic_light, intersection, traffic_manager, statistics, simulation, comparison
    ai/                       traffic_controller (Fixed/Smart), traffic_score, priority_system
    ui/                       renderer (الرسم), dashboard (اللوحة والأزرار)

## التوسع لاحقاً
`ai/traffic_controller.py` يعرّف واجهة صغيرة (`green_time`, `should_end_green`, `choose_next_axis`).
يمكن استبدال `SmartController` بمتحكم ML/RL، ومصدر `traffic.metrics` بعدّاد YOLO/كاميرا
دون تغيير الـSimulation أو الـUI. لإضافة Left/Right turns أو مسارات متعددة: عمّم `Car.x/y` إلى مسارات (waypoints).
