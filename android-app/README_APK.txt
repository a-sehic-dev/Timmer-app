ANDROID APK — Build Instructions
================================

The timer web app is bundled inside a native Android shell (Capacitor).
Result: fully OFFLINE APK — no server, no internet needed after install.

REQUIREMENTS (one-time)
-----------------------
1. Node.js (already installed)
2. Android Studio — https://developer.android.com/studio
   (installs Java JDK + Android SDK automatically)

BUILD STEPS
-----------
1. Open terminal in this folder: android-app

2. Install dependencies:
   npm install

3. Add Android platform (first time only):
   npx cap add android

4. Sync web files into Android project:
   npx cap sync android

5. Build debug APK:
   cd android
   gradlew.bat assembleDebug

6. APK location:
   android\app\build\outputs\apk\debug\app-debug.apk

   Rename to TimerApp.apk and send to client.

INSTALL ON CLIENT'S ANDROID PHONE
---------------------------------
1. Copy TimerApp.apk to phone (email, Drive, USB)
2. Settings → Security → Allow install from unknown sources
3. Tap APK → Install
4. Open "Timer" app — works offline

NO Google Play needed. NO $99 Apple account. FREE sideload.
