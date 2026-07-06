# 📋 プロジェクトメモ：量子コンピューター 現在地調査
**最終更新：** 2026年07月06日

---

## 作成済みファイル

| ファイル名 | 内容 |
|---|---|
| `quantum_roadmap.html` | 実用化ロードマップ全体（タイムライン・NVIDIAバナー・応用領域マトリクス） |
| `quantum_by_type.html` | 方式別・企業別マイルストーン（タブ切り替えUI・6タブ） |

---

## 調査の核心：NVIDIA Ising＋NVAQC（2026年4月14日発表）

- **Ising Calibration**（35B VLM）：量子キャリブレーション自動化。数日→数時間に短縮
- **Ising Decoding**（3D CNN）：誤り訂正デコード。速度2.5×・精度3×向上
- **NVIDIA NVQLink**：QPU-GPU リアルタイム接続。17 QPUベンダー / 5制御ベンダー / 9米国立研と統合
- **NVAQC（NVIDIA Accelerated Quantum Research Center）**：ボストン新設の量子加速研究所 ★NEW
- **採用機関**：Academia Sinica・Fermilab・Harvard・Infleqtion・IQM・LBNL・英NPL等
- **市場反応**：IonQ・D-Wave +50%、Xanadu +250%

---

## 量子コンピューター 5方式サマリー

| 方式 | 主要企業 | 現在地（2026） | FTQC予測 |
|---|---|---|---|
| ⚡ 超伝導型 | IBM / Google / 富士通×理研 / 叡-Ⅱ / Rigetti | Nighthawk 7,500ゲート / Kookaburra QECモジュール / 叡-Ⅱ 144QB稼働 | 2028〜2029（IBM Starling） |
| 🔬 イオントラップ型 | IonQ / Quantinuum | 12論理QB・99.99%精度 / Q-CTRL統合 / QLDPC新設計 | 2027〜2029 |
| 🔷 トポロジカル型 | Microsoft（Majorana 1）/ 東北大 | Lyngby（デンマーク）量子ラボ開設 / Magne建設中 | 2030年代 |
| ⚛️ 中性原子型 | Atom Computing×MS / QuEra | QuEra×Harvard×MIT 2:1物理-論理QB比達成 / Magne 50論理QB予定 | 2026〜2027 |
| 💡 光量子型 | PsiQuantum / Xanadu / NTT | Xanadu Aurora（12論理GKP）／IPO上場（XNDU $302M）／NTT IOWN 2.0 | 2028〜2030 |

---

## 日本エコシステム

- **富士通×理研**：超伝導型。2025秋に川崎・量子棟 竣工、2026年度に1,000QB設置・公開。2030年に1万QB超
- **理研×大阪大QIQB**：「叡-Ⅱ」144QB（28×28mm 2D配置）が2026年3月26日 運用開始 ★NEW
- **NTT**：光量子型。2025年11月 OptQCと連携協定 → 2026年1月 IOWN Tech Report公開 → FY2026 PEC-2「光エンジン」商用化（IOWN 2.0始動）→ 2030年100万QB目標
- **NTTデータ**：量子SIer。PQC対応・CUDA-Q活用ハイブリッド実装支援
- **産総研 G-QuAT**：方式横断ハブ。QuEra（37論理QB / 260物理QB）導入・Intel MOU・2026年3月 光量子顕微鏡テストベッド開設 ★NEW
- **東北大学**：2026年4月23日、量子スピン液体から電気信号抽出に世界初成功（トポロジカルQC基盤） ★NEW
- **PsiQuantum × 東大 × 三菱ケミカル**：NEDO支援 FTQC人材育成プログラム（80名/20社）

---

## 企業別 主要マイルストーン

- **IBM**：2026年量子優位性目標 / Nighthawk 7,500ゲート・360QB / Kookaburra（初のQEC対応モジュール、LDPC符号）→ 2028-29年 Starling（200論理QB / 10,000物理QB / 1億ゲート） / Albany NanoTech 300mmウェハー製造 → 2030年代 Blue Jay（1万QB超）
- **Google**：2024年Willowチップ・量子優位性実証済み
- **Microsoft**：2025年2月 Majorana 1発表 → 2026年春 Lyngby（デンマーク）量子ラボ開設（$140M+） → 2026年末-2027年初 Magne稼働（50論理QB / ~1,200物理QB）
- **IonQ**：2026年4月18日 SDT（韓国）資源連携協定 → 4月22日 QLDPC「Walking Cat」新ブループリント → 4月24日 Q-CTRL Fire Opal 統合 → 12論理QB → 2027年1万QB単一チップ → 2028年CRQC ★NEW
- **Xanadu**：2026年3月27日 Nasdaq+TSX上場（XNDU、$302M調達）→ 4月 Aurora（モジュラー光量子コンピューター・12論理GKP）→ DARPA QBI ステージB（最大$15M）/ カナダ Quantum Champions（最大CAD$23M） ★NEW
- **PsiQuantum**：GlobalFoundriesと光チップ量産中 → 東大×三菱ケミカルとNEDO支援FTQC人材育成 → 2027〜29年100万QB FTQC目標
- **QuEra**：2026年4月 Harvard×MITと2:1物理-論理QB比達成（QLDPC符号）／ 4月3日 OSS論理量子回路シミュレータ公開／2026年100論理QB・10,000物理QB目標 ★NEW
- **産総研**：2024年内閣総理大臣賞（超伝導QC基盤）・QuEra導入・Intel MOU締結・2026年3月 光量子顕微鏡テストベッド開設

---

## 実用化タイムライン概観

- **2026年（現在）**：NISQ→FTQC移行期。品質・誤り訂正精度が競争軸
- **2026〜2027年初**：Microsoft Magne（50論理QB）稼働予定
- **2027〜2029年**：量子-古典ハイブリッドの産業応用本格化
- **2028〜2029年**：IBM Starling 投入（200論理QB / 10,000物理QB / 1億ゲート）
- **2030年代**：本格的フォールトトレラント実用期（数万論理QB）
