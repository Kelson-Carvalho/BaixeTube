import os, sys

proj = sys.argv[1]
bg   = os.path.join(proj, "app", "build.gradle")

linhas = [
    "def buildAsLibrary = project.hasProperty('BUILD_AS_LIBRARY');",
    "def buildAsApplication = !buildAsLibrary",
    "if (buildAsApplication) {",
    "    apply plugin: 'com.android.application'",
    "}",
    "else {",
    "    apply plugin: 'com.android.library'",
    "}",
    "",
    "android {",
    "    namespace 'org.baixetube'",
    "    compileSdkVersion 34",
    "    defaultConfig {",
    "        if (buildAsApplication) {",
    '            applicationId "org.baixetube"',
    "        }",
    "        minSdkVersion 26",
    "        targetSdkVersion 34",
    "        versionCode 1",
    '        versionName "1.0"',
    "    }",
    "    buildTypes {",
    "        release {",
    "            minifyEnabled false",
    "            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'",
    "        }",
    "    }",
    "    lintOptions {",
    "        abortOnError false",
    "    }",
    "}",
    "",
    "dependencies {",
    "    implementation fileTree(include: ['*.jar'], dir: 'libs')",
    "}",
]

novo = "\n".join(linhas) + "\n"

with open(bg, "w") as f:
    f.write(novo)

print("build.gradle substituido com sucesso!")
print(open(bg).read())
