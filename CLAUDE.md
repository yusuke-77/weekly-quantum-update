# 📋 プロジェクトメモ：量子コンピューター 現在地調査
**最終更新：** 2026年09月14日

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
| ⚡ 超伝導型 | IBM / Google / 富士通×理研 / 叡-Ⅱ / Rigetti | **IBM×Qedma 74QBで量子優位性実証（7/30）** / Nighthawk 7,500ゲート / Kookaburra QECモジュール / 叡-Ⅱ 144QB稼働 / Willow 論理エラー率 7.72×10⁻⁴ | 2028〜2029（IBM Starling） |
| 🔬 イオントラップ型 | IonQ / Quantinuum | 12論理QB・99.99%精度 / IonQ QEC 9コード実証（6/6）・Duke大 3ノード分散もつれ / Quantinuum QNT上場完了$1.68B（6/4）/ MS×Quantinuum Nature 800倍エラー削減（6/12）/ Sandia が Helios 98QB 第三者検証 2QB 99.921%（6/17） | 2027〜2029 |
| 🔷 トポロジカル型 | Microsoft（Majorana 1→2）/ 東北大 / **Quantinuum（エニオン方式）** | Majorana 2 発表（6/2）量子ビット寿命20秒・1,000倍信頼性・2029年目標 / **Quantinuum×シカゴ大が H2 上で万能トポロジカルゲートセット実証（7/15 Nature）— 物理マヨラナ不要のソフト実装路線** | 2029〜2030年代 |
| ⚛️ 中性原子型 | Atom Computing×MS / QuEra | QuEra×Harvard×MIT 2:1物理-論理QB比達成 / Magne 50論理QB予定 | 2026〜2027 |
| 💡 光量子型 | PsiQuantum / Xanadu / NTT | Xanadu Aurora（12論理GKP）／IPO上場（XNDU $302M）／NTT IOWN 2.0 | 2028〜2030 |

---

## 日本エコシステム

- **富士通×理研**：超伝導型。2025秋に川崎・量子棟 竣工、2026年度に1,000QB設置・公開。2030年に1万QB超
- **理研×大阪大QIQB**：「叡-Ⅱ」144QB（28×28mm 2D配置）が2026年3月26日 運用開始 ★NEW
- **NTT**：光量子型。2025年11月 OptQCと連携協定 → 2026年1月 IOWN Tech Report公開 → FY2026 PEC-2「光エンジン」商用化（IOWN 2.0始動）→ 2030年100万QB目標
- **NTTデータ**：量子SIer。PQC対応・CUDA-Q活用ハイブリッド実装支援
- **産総研 G-QuAT**：方式横断ハブ。QuEra（37論理QB / 260物理QB）導入・Intel MOU・2026年3月 光量子顕微鏡テストベッド開設・NVIDIA支援の ABCI-Q（世界最大の量子研究専用スパコン：富士通超伝導+QuEra中性原子+OptQC光量子のハイブリッドQPU環境）開設 ★NEW
- **日立 × Intel × 産総研**：2026年7月24日、シリコン量子コンピューターの共同研究開発を開始（NEDO採択・実施期間2029年3月まで）。2030年度に1,000量子ビット級の誤り耐性型シリコン量子コンピューター試作機を目指す。国内に「シリコンスピン型」の方式軸が追加 ★NEW
- **東北大学**：2026年4月23日、量子スピン液体から電気信号抽出に世界初成功（トポロジカルQC基盤）
- **PsiQuantum × 東大 × 三菱ケミカル**：NEDO支援 FTQC人材育成プログラム（80名/20社）
- **東陽テクニカ × IQM**：2026年4月27日、IQM Radiance（20量子ビット・フルスタック）を購入決定。日本企業が商用量子コンピューターを自社購入する初事例。2026年末納入 ★NEW

---

## 企業別 主要マイルストーン

- **IBM**：2026年量子優位性目標 / Nighthawk 7,500ゲート・360QB / Kookaburra（初のQEC対応モジュール、LDPC符号）→ 4/15 Voyager Spaceと地球-ISS PQC通信 世界初成功（Quantum Safe Remediator）／ParityQC「Parity Twine」で Heron r3 上 52量子ビット QFT 実行／Algorithmiq×Cleveland Clinic Q4Bio $2M受賞 → 4/28 Poughkeepsie 量子キャンパス511,000㎡拡張申請（Starling製造施設）→ 5/4 クラウド量子10周年 → 5/5 Cleveland Clinic×RIKEN×IBMが12,635原子タンパク質シミュレーション世界最大記録（Heron r3 156QB + 富岳 + Miyabi-G）→ 5/21 米国商務省とCHIPS法補助金$1Bで「Anderon」量子ファウンドリー設立発表（Albany NY）、IBM株翌日+12% → 5/28 今後5年間で$10B超の量子投資計画を表明 → 6/12 ffsim OSS公開（フェルミオン回路高速シミュレーター）→ 6/13 OpenEvolve OSS公開（LLM誘導でQECコード候補465種発見）→ 6/20 Nighthawk 独立研究2件で検証（粒子物理シミュレーション・サイバーセキュリティ最適化）→ 6/29 Qiskit Paulice OSS公開（spacetime Pauliチェック誤り検出・50QB実証）→ 7月 インド Andhra Pradesh州 Amaravati「Quantum Valley」に IBM Quantum System Two（Heron 156QB）設置決定・2026年9月稼働予定 → 7月 ORNL×Cleveland Clinic×IBM が核融合向け FLiBe溶融塩トリチウム結合の量子-古典シミュレーション世界初成功（DOE Genesis Mission）→ **7/23 HRL Laboratories 買収発表（Boeing・GM 共同出資／シリコンスピン量子ビット・量子センシング／HRLは4月に54量子ドット・18QBのSiプロセッサ公表／Q3末クローズ予定・金額非開示）★NEW** → **7/30 Qedma と量子優位性を実証：QESEM 誤り緩和＋IBM機で 2D Floquet Ising の振動ダイナミクスを最大74QBで解析、富岳を含む古典手法が一貫結果を出せない領域で trusted 計算を達成 ★NEW** → 2028-29年 Starling（200論理QB / 10,000物理QB / 1億ゲート） / Albany NanoTech 300mmウェハー製造 → 2030年代 Blue Jay（1万QB超）
- **Google**：2024年Willowチップ・量子優位性実証済み → 2026年3月24日 中性原子型へロードマップ拡張（Adam Kaufman主導）→ 3月28日 Willow Early Access Program 開始 → 5/15 同プログラム締切 完了 → 5月 REPLIQA プログラム始動（量子AI×生命科学・$10M、タンパク質フォールディング・薬物代謝シミュレーション）→ **7月 Willow 表面符号 論理エラー率 7.72×10⁻⁴/サイクル記録更新（強化学習HW制御フレームワーク）・Fraunhofer INQUBATOR と early-FTQC 世界公募開始（最大$100K・8/7締切）★NEW**
- **Microsoft**：2025年2月 Majorana 1発表 → 2026年春 Lyngby（デンマーク）量子ラボ開設（$140M+） → **6/2 Majorana 2 発表（Al→Pb置換・トポロジカルギャップ2倍・量子ビット寿命20秒・1,000倍信頼性・2029年スケーラブルQC目標）★NEW** → 2026年末-2027年初 Magne稼働（50論理QB / ~1,200物理QB）
- **Quantinuum × Microsoft**：System Model H2 が世界初の Microsoft Level 2「Resilient」フェーズ到達 → 4/14 H2 を理研「Reimei-Fugaku」へ納入 → 4/22 Honeywell Form S-1 機密申請 → 5/2 量子 qMCMC 世界初ハードウェア実行 → 5/5 BMW Group 多年間提携 → 5/8 Nasdaq S-1 正式提出 → 5/26 IPO公開価格決定 → 6/4 Nasdaq（QNT）上場完了・$1.68B調達（$60/株・2,800万株）・初値+13%・評価額$14-15B → 6/5 三菱電機 MOU締結 → 6/12-13 MS×Quantinuum 誤り訂正 Nature 掲載論文（11〜800倍エラー率削減・deq OSSライブラリ公開）→ 6/17 Sandia国立研が Helios 98QB を第三者検証（1QB 99.9975%・2QB 99.921%・SPAM 99.967%、peer-review）→ **7/15 シカゴ大PME×Harvard×Stony Brook と世界初の万能トポロジカルゲートセットを Nature 発表（H2 で54QBもつれ・S3非可換エニオンのブレイディング＋fusion・magic state distillation 不要）★NEW** → **7/21 SoftBank と企業導入ロードマップ白書（Helios→Sol 2027→Apollo 2029→Lumos 2030年代）★NEW**
- **IonQ**：2026年4月14日 フォトニック・インターコネクト実証（DARPA HARQ）→ 4/18 SDT（韓国）資源連携協定 → 4/22 QLDPC「Walking Cat」新ブループリント → 4/24 Q-CTRL Fire Opal 統合 → 4/27 Florida LambdaRail QSN提携 → 4/9 Horizon Quantum に Tempo 出荷決定 → 5/1 Jeff Henshaw SVP就任 → 5/6 Q1売上 $64.7M（前年比755%増）→ 5/14 Boulder量子研究所開設 → 6/6 9種類のQECコードをイオントラップ上で一挙実証 → 6/11 Tempo 256QB を Horizon Quantum ダブリン欧州拠点に設置 → **6月 Duke大と3ノード量子ネットワークで分散三者間もつれ実証（モジュラーQC枠組み確立）★NEW** → **6月 Fixstars Amplify に量子シミュレーター統合（日米で組合せ最適化）★NEW** → **7/1 Archer Materials と豪州展開 $1.5M 契約（オンショア配備調査・QML不正検知）★NEW** → SkyWater合併（株主承認済み・規制認可待ち Q2/Q3）→ 2027年1万QB単一チップ → 2028年CRQC
- **Xanadu**：2026年3月27日 Nasdaq+TSX上場（XNDU、$302M調達）→ 4月 Aurora（モジュラー光量子コンピューター・12論理GKP）→ DARPA QBI ステージB（最大$15M）/ カナダ Quantum Champions（最大CAD$23M）
- **PsiQuantum**：GlobalFoundriesと光チップ量産中 → 東大×三菱ケミカルとNEDO支援FTQC人材育成 → 2027〜29年100万QB FTQC目標
- **QuEra**：2026年4月 Harvard×MITと2:1物理-論理QB比達成（QLDPC符号）／ 4月3日 OSS論理量子回路シミュレータ公開／2026年100論理QB・10,000物理QB目標
- **産総研**：2024年内閣総理大臣賞（超伝導QC基盤）・QuEra導入・Intel MOU締結・2026年3月 光量子顕微鏡テストベッド開設
- **東陽テクニカ**：2026年4月27日、IQM Radiance（20量子ビット）を購入。日本企業初の量子コンピューター自社購入。2026年末納入予定 ★NEW

---

## 米国 CHIPS法 量子投資（2026年5月21日）

- **総額 $2.013B**：米国商務省が量子9社へ LOI を通知。政府は各社に少数株持分を取得
- IBM $1B（Anderon ファウンドリー）/ GlobalFoundries $375M / D-Wave・Infleqtion $100M ずつ / Diraq $38M
- Quantinuum・PsiQuantum・Atom Computing・Rigetti にも最大 $100M ずつ
- 発表後、IonQ +12%・量子株全面高

---

## 米大統領令2本＋国防総省の量子シフト（2026年6月22日〜7月1日）

- **6/22 EO 14413「量子イノベーションの次のフロンティア」**：QC-ADDS 構想。DOE・国防・商務・情報機関横断で**2028年までに科学発見級量子コンピューターをDOE施設に納入**目標。国家量子戦略更新（180日以内）・人材育成・国内サプライチェーン・量子センサー5年配備計画も指示
- **6/22 EO 14412「高度暗号攻撃からの防衛」**：連邦システムの PQC 移行を2030年（鍵確立）／2031年（電子署名）までに義務化。2030年末までに FAR で連邦契約企業にも PQC 準拠要求
- **市場反応**：6/23 量子株急騰。Rigetti 約$22.65・D-Wave 約$26.30（時間外）。「$2B支援の物語」→「連邦の具体的タイムライン」へ転換と評価
- **7/1 国防総省 PQC戦略**：軍事システムの暗号脆弱性を2031年末までに排除
- **7/1 DIU「Project Farseer」**：$200M で量子センシング・タイミングHWの軍事実装を加速
- **6/22 Infleqtion「America's Quantum Space Initiative」**：Voyager Technologies・コロラド大ボルダー校らと官民連合発足（航空宇宙×量子）

---

## 前週の動き（6/22〜7/2）

- **6/23 IQM**：新QECアーキテクチャ「Directional Tile Codes」発表。表面符号比で物理-論理オーバーヘッド最大1,000分の1。平面実装可能
- **6/26 Pasqal**：中性原子QPUのHPCデータセンター統合。OSSオーケストレーション層「Warden」＋QRMI仕様公開
- **6/22 Fraunhofer IPMS**：QRNG「Q-Dice」（4.1 Gbit/s超・量子真空ゆらぎ測定）

---

## 🗓 2026年7月 月次サマリー（7/1〜7/31）★NEW

### 今月の最大トピック

- **7/30 IBM × Qedma「量子優位性」実証**：QESEM 誤り緩和＋IBM機で 2D Floquet Ising モデルの長寿命振動ダイナミクスを最大74QBで解析。理研「富岳」を含む最先端古典シミュレーションが一貫した結果を出せない規模で trusted 計算を達成。IBM の「2026年 量子優位性」目標の中核成果
- **7/15 Quantinuum × シカゴ大PME × Harvard × Stony Brook（Nature）**：世界初の万能トポロジカルゲートセット。H2 で54QBもつれ・S3非可換エニオンのブレイディング＋fusion。magic state distillation 不要の万能量子計算への道
- **7/23 IBM が HRL Laboratories 買収**：シリコンスピン量子ビット＋量子センシングを獲得。超伝導との二刀流化、Anderon ファウンドリーでのスピン量子ビット製造も視野

### 産業・市場

- **7/27 D-Wave**：NYSE→Nasdaq Global Select Market（QBTS）へ上場移管。同日 AT&T が複数年契約を拡大（障害検知・技術者派遣計画・トラフィック管理／初期案件で約1時間→15秒未満の240倍加速）。株価当日+20.36%（$19.51）
- **7/21 Quantinuum × SoftBank**：企業導入ロードマップ白書（Helios→Sol 2027→Apollo 2029→Lumos 2030年代）
- **7/1 Archer Materials × IonQ**：豪州展開 $1.5M 契約（オンショア配備調査・QML不正検知）
- **7/9 qBraid × Quantum Rings**：数万ユーザーに$50無料QPUクレジット（IonQ・Rigetti・IQM・AQT接続）
- **7月 SEALSQ × Quobly**：$5M でシリコンスピン量子プロセッサに PQC 統合 / SAS が Viya 上に「Quantum Lab」開設（classical-first検証）

### 国家・政策

- **7/1 米国防総省**：PQC戦略（軍事システムの暗号脆弱性を2031年末までに排除）＋ DIU「Project Farseer」$200M（量子センシング・タイミングHWの軍事実装）
- **7/24 日立 × Intel × 産総研**：NEDO採択でシリコン量子コンピューター研究開発を開始。2030年度に1,000QB級の誤り耐性型試作機（実施期間2029年3月まで）。国内に「シリコンスピン型」の方式軸が加わる
- **7月 インド**：Amaravati「Quantum Valley」に IBM Quantum System Two（Heron 156QB）設置決定・9月稼働予定
- **7月上旬 韓国**：Quantum Korea 2026 で加・英・EUと多国間枠組み / QAI Ventures シンガポール量子アクセラレーター開始（4社×SGD 30万）
- **7月 Chips JU × Pasqal**：€50M「Q-PLANET」始動。中性原子量子チップの汎欧州製造基盤

### 技術・研究

- **7月 Google Willow**：表面符号 論理エラー率 7.72×10⁻⁴/サイクル記録更新（強化学習HW制御）。Fraunhofer INQUBATOR と early-FTQC 世界公募（最大$100K・8/7締切）
- **7月 ORNL × Cleveland Clinic × IBM**：核融合向け FLiBe溶融塩トリチウム結合の量子-古典シミュレーション世界初成功（DOE Genesis Mission）
- **7/10 ETH Zurich**：「振動量子RAM」実証（超伝導QB×機械共振器で量子情報を音響振動として格納）
- **7/10 EeroQ**：超流動ヘリウム上の電子シャトリング成功（electron-on-helium 方式の無損失長距離輸送）
- **7月 理論**：spectral forrelation 問題で「量子証明は古典証明で代替不可」を初証明（Zhandry・Bostanci・Haferkamp・Nirkhe ら）

### 継続ウォッチ

- **IonQ × SkyWater 合併**：7月末時点で未完了（規制認可待ち・Q3クローズ予定）
- **IBM × HRL 買収**：Q3末クローズ予定
- **富士通×理研 1,000QB**：2026年度中に量子棟へ設置・公開予定

---

## 実用化タイムライン概観

- **2026年（現在）**：NISQ→FTQC移行期。品質・誤り訂正精度が競争軸。**7/30 IBM×Qedma が74QBで量子優位性を実証し、「優位性の証明」フェーズは達成局面へ**
- **2026〜2027年初**：Microsoft Magne（50論理QB）稼働予定
- **2027〜2029年**：量子-古典ハイブリッドの産業応用本格化
- **2028〜2029年**：IBM Starling 投入（200論理QB / 10,000物理QB / 1億ゲート）
- **2030年代**：本格的フォールトトレラント実用期（数万論理QB）
