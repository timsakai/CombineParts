説明
blender 4.2 向けアドオン。
fbx出力時など、肥大化しがちなオブジェクト(ノード)数を削減するスクリプト。
ワンクリックで大量のオブジェクトを自動で結合、出力のために最適化。
Unityなどで、ドローコールが増えてしまう原因となる複雑なモデルを、Blender側からメッシュベイク。blender上なので、ベイク結果を編集可能。

使用法
インストール　：　Preferences > Add-ons > Install from Disk　からzipを指定、CombinePartsにチェックで有効化
場所 　：　Nパネル（プロパティサイドバー）>  CombineParts

①CombineParts > "Setup Collection"　で、処理対象指定・処理結果保存用のコレクション、"Parts","Combined"を作成します。

②"Parts" 内に、結合したいメッシュオブジェクトを登録してください。（"Parts"内にさらにお好みのコレクションをネスト可能）

③CombineParts > "Run Combine" で、"Parts"内のオブジェクトを結合します。
　"Parts_combined" という名前で保存されます。

仕様　：
①Mirrorモディファイア付きオブジェクトは、"Parts_mirror_combined"という名前で分割、Mirrorモディファイアを非適用で保存されます。

②頂点グループウェイト・アーマチュアモディファイアとアーマチュアの指定は維持されます。

③結合処理はBlenderのオブジェクト結合操作を使用しています。
