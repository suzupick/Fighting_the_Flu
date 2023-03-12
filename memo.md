# TODO
 - ゲームクリア時のスコアに応じて笑顔の澤口を表示する
 - リファクタリング（設計を見直して、Gameクラス、Playerクラス、Enemyクラスなどの実装）
 - 敵弾の実装
 - 敵機HP、自機HP
 - パワーアップ要素
 - 自機同時2機操縦


# ビルド方法
## 仮想環境アクティベート：
.venv/Scripts/Activate.ps1

## Pyinstallerのビルド方法：
1. コンパイラ(？)のインストール
choco install -y visualstudio2019-workload-vctools

2. PyInstallerのリポジトリをクローン
git clone https://github.com/pyinstaller/pyinstaller

3. PyInstallerをソースからビルド
ブートローダーのフォルダに移動し
[python] ./waf all
※[python]は仮想環境のpythonを使う

PyInstallerビルド方法参考ページ：
https://pyinstaller.org/en/latest/bootloader-building.html


## プログラムのビルド：
pyinstaller game.py --onefile