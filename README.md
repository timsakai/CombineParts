<img src="https://imgur.com/a/rtH2lvS" alt="サムネ" title="サムネ">
# 説明
blender 4.2 向けアドオン。
fbx出力時など、肥大化しがちなオブジェクト(ノード)数を削減するスクリプト。
ワンクリックで大量のオブジェクトを自動で結合、出力のために最適化。
Unityなどで、ドローコールが増えてしまう原因となる複雑なモデルを、Blender側からメッシュベイク。blender上なので、ベイク結果を編集可能。

# 使用法
## インストール
 - references > Add-ons > Install from Disk　からzipを指定、CombinePartsにェックで有効化
## 場所 
 - Nパネル（プロパティサイドバー）>  CombineParts

1. CombineParts > "Setup Collection"　で、処理対象指定・処理結果保存用のコレクション、"Parts","Combined"を作成します。

2. "Parts" 内に、結合したいメッシュオブジェクトを登録してください。（"Parts"内にさらにお好みのコレクションをネスト可能）

3. CombineParts > "Run Combine" で、"Parts"内のオブジェクトを結合します。
　"Parts_combined" という名前で保存されます。
<img src="https://raw.githubusercontent.com/timsakai/CombineParts/refs/heads/main/preaseIgone_packing/CombinePartsDescription/InstallUsage.png?token=GHSAT0AAAAAAC2DRIPTUHJGY7U5DCPINL6KZZ6ZG5A" alt="説明" title="説明">
# 仕様
- Mirrorモディファイア付きオブジェクトは、"Parts_mirror_combined"という名前で分割、Mirrorモディファイアを非適用で保存されます。

- 頂点グループウェイト・アーマチュアモディファイアとアーマチュアの指定は維持されます。

# 仕組み
- 結合処理はBlenderのオブジェクト結合操作を使用しています。
- コア機能はCombine.pyに集約しています。
- Blenderの標準的な機能で、ボタンの登録、及びボタンへの機能の登録を行っています。
- メインの機能は、blenderのpythonログをベースに作成しました。
- コレクションをネスト可能にするために、再帰的にオブジェクトのリストをとってくる関数を作成しました。
- 処理前に、リンクを解除し、対象をTempコレクションにコピーします。よって、元データを破壊することはありません
