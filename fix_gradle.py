import os
import sys

proj = sys.argv[1]
bg = os.path.join(proj, "app", "build.gradle")

novo = (
    "def buildAsLibrary = project.hasProperty('BUILD_AS_LIBRARY');\n"
    "def buildAsApplication = !buildAsLibrary\n"
    "if (buildAsApplication) {\n"
    "    apply plugin: 'com.android.application'\n"
    "}\n"
    "else {\n"
    "    apply plugin: 'com.android.library'\n"
    "}\n"
    "\n"
    "android {\n"
    "    compileSdkVersion 34\n"
    "    defaultConfig {\n"
    "        if (buildAsApplication) {\n"
    '            applicationId "org.baixetube"\n'
    "        }\n"
    "        minSdkVersion 26\n"
    "        targetSdkVersion 34\n"
    "        versionCode 1\n"
    '        versionName "1.0"\n'
    "    }\n"
    "    buildTypes {\n"
    "        release {\n"
    "            minifyEnabled false\n"
    "            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'\n"
    "        }\n"
    "    }\n"
    "    lintOptions {\n"
    "        abortOnError false\n"
    "    }\n"
    "}\n"
    "\n"
    "dependencies {\n"
    "    implementation fileTree(include: ['*.jar'], dir: 'libs')\n"
    "}\n"
)

with open(bg, "w") as f:
    f.write(novo)

print("build.gradle substituido!")
print(open(bg).read())
