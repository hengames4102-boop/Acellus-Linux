import sys, json
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEngineScript, QWebEnginePage

URL = "https://signin.acellus.com/app"

class Page(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, msg, line, source):
        print(f"[JS] {msg}")

app = QApplication(sys.argv)

profile = QWebEngineProfile.defaultProfile()
profile.setHttpUserAgent(profile.httpUserAgent() + " /Android_Acellus_V2.035")

script = QWebEngineScript()
script.setName("FakeAndroidBridge")
script.setInjectionPoint(QWebEngineScript.InjectionPoint.DocumentCreation)
script.setWorldId(QWebEngineScript.ScriptWorldId.MainWorld)
script.setRunsOnSubFrames(True)
script.setSourceCode(r"""
window.Android = {
  notify: function(x){ console.log("Android.notify:", x); },
  printPage: function(x){ console.log("Android.printPage:", x); window.print(); },
  printCertificate: function(x){ console.log("Android.printCertificate:", x); window.print(); },
  reactBluetoothMessage: function(x){ console.log("Android.reactBluetoothMessage:", x); },
  handleTouchEvent: function(x){ console.log("Android.handleTouchEvent:", x); },
  onBlobFetched: function(){ console.log("Android.onBlobFetched"); }
};
console.log("Fake window.Android bridge loaded");
""")
profile.scripts().insert(script)

view = QWebEngineView()
view.setPage(Page(profile, view))
view.load(QUrl(URL))
view.showMaximized()

sys.exit(app.exec())
