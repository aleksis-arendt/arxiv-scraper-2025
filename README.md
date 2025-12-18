# arXiv Reader (Local Research Tool)

**arXiv Reader** là một công cụ chạy cục bộ giúp tìm kiếm, lọc và quản lý bài báo từ arXiv theo từng lĩnh vực nghiên cứu như *Mathematics, Physics, Computer Science* và *Quantitative Biology*.

Ứng dụng được thiết kế cho mục đích học thuật và nghiên cứu cá nhân:
- Chạy hoàn toàn **local** trên máy người dùng
- Không yêu cầu tài khoản
- Không upload dữ liệu cá nhân lên server bên ngoài
- Phù hợp cho sinh viên, nghiên cứu sinh và giảng viên

Giao diện được xây dựng bằng **Streamlit**, chạy trong trình duyệt web mặc định của hệ thống.
## Cách chạy

### Yêu cầu hệ thống
- Windows 10 / 11
- Python 3.9 trở lên
- Kết nối Internet (để truy vấn arXiv và tải PDF)

### Các bước
1. Mở thư mục ứng dụng
2. Double-click file `run_me.bat`
3. Ứng dụng sẽ tự động:
   - Kiểm tra Python
   - Cài các thư viện cần thiết 
   - Mở giao diện trong trình duyệt

Sau khi chạy thành công, giao diện sẽ mở tại:
http://localhost:8501
## Hướng dẫn sử dụng

### 1. Chọn lĩnh vực và chủ đề
Ở panel bên trái:
- Chọn **Domain** (Mathematics, Physics, Computer Science, ...)
- Chọn **Topic** (ví dụ: Differential Geometry, General Relativity, Machine Learning)

Ứng dụng sẽ tự động sinh truy vấn arXiv tương ứng (`cat:math.DG`, `cat:gr-qc`, ...).

### 2. Chạy crawler
- Điều chỉnh khoảng thời gian (Start date / End date)
- Chọn số lượng bài tối đa
- Nhấn **Run spider**

Kết quả sẽ được lưu thành snapshot JSON trong thư mục `runs/`.

### 3. Lọc và xếp hạng bài báo
- Nhập danh sách từ khóa để xếp hạng (keywords)
- Điều chỉnh thanh **Minimum score**
- Các bài có điểm cao hơn sẽ được ưu tiên hiển thị

### 4. Chọn bài quan tâm
- Dùng checkbox để chọn từng bài
- Hoặc chọn **Select all**

## Physics

- **astro-ph** — Astrophysics  
  - astro-ph.GA — Astrophysics of Galaxies  
  - astro-ph.CO — Cosmology and Nongalactic Astrophysics  
  - astro-ph.EP — Earth and Planetary Astrophysics  
  - astro-ph.HE — High Energy Astrophysical Phenomena  
  - astro-ph.IM — Instrumentation and Methods for Astrophysics  
  - astro-ph.SR — Solar and Stellar Astrophysics  

- **cond-mat** — Condensed Matter  
  - cond-mat.dis-nn — Disordered Systems and Neural Networks  
  - cond-mat.mtrl-sci — Materials Science  
  - cond-mat.mes-hall — Mesoscale and Nanoscale Physics  
  - cond-mat.other — Other Condensed Matter  
  - cond-mat.quant-gas — Quantum Gases  
  - cond-mat.soft — Soft Condensed Matter  
  - cond-mat.stat-mech — Statistical Mechanics  
  - cond-mat.str-el — Strongly Correlated Electrons  
  - cond-mat.supr-con — Superconductivity  

- **gr-qc** — General Relativity and Quantum Cosmology  

- **hep-ex** — High Energy Physics – Experiment  
- **hep-lat** — High Energy Physics – Lattice  
- **hep-ph** — High Energy Physics – Phenomenology  
- **hep-th** — High Energy Physics – Theory_toggle

- **math-ph** — Mathematical Physics  

- **nlin** — Nonlinear Sciences  
  - nlin.AO — Adaptation and Self-Organizing Systems  
  - nlin.CG — Cellular Automata and Lattice Gases  
  - nlin.CD — Chaotic Dynamics  
  - nlin.SI — Exactly Solvable and Integrable Systems  
  - nlin.PS — Pattern Formation and Solitons  

- **nucl-ex** — Nuclear Experiment  
- **nucl-th** — Nuclear Theory  

- **physics** — General Physics  
  - physics.acc-ph — Accelerator Physics  
  - physics.app-ph — Applied Physics  
  - physics.ao-ph — Atmospheric and Oceanic Physics  
  - physics.atom-ph — Atomic Physics  
  - physics.atm-clus — Atomic and Molecular Clusters  
  - physics.bio-ph — Biological Physics  
  - physics.chem-ph — Chemical Physics  
  - physics.class-ph — Classical Physics  
  - physics.comp-ph — Computational Physics  
  - physics.data-an — Data Analysis, Statistics and Probability  
  - physics.flu-dyn — Fluid Dynamics  
  - physics.gen-ph — General Physics  
  - physics.geo-ph — Geophysics  
  - physics.hist-ph — History and Philosophy of Physics  
  - physics.ins-det — Instrumentation and Detectors  
  - physics.med-ph — Medical Physics  
  - physics.optics — Optics  
  - physics.plasm-ph — Plasma Physics  
  - physics.pop-ph — Popular Physics  
  - physics.soc-ph — Physics and Society  
  - physics.space-ph — Space Physics  
  - physics.ed-ph — Physics Education  

- **quant-ph** — Quantum Physics  
## Mathematics

- **math** — Mathematics  
  - math.AG — Algebraic Geometry  
  - math.AT — Algebraic Topology  
  - math.AP — Analysis of PDEs  
  - math.CT — Category Theory  
  - math.CA — Classical Analysis and ODEs  
  - math.CO — Combinatorics  
  - math.AC — Commutative Algebra  
  - math.CV — Complex Variables  
  - math.DG — Differential Geometry  
  - math.DS — Dynamical Systems  
  - math.FA — Functional Analysis  
  - math.GM — General Mathematics  
  - math.GN — General Topology  
  - math.GT — Geometric Topology  
  - math.GR — Group Theory  
  - math.HO — History and Overview  
  - math.IT — Information Theory  
  - math.KT — K-Theory and Homology  
  - math.LO — Logic  
  - math.MP — Mathematical Physics  
  - math.MG — Metric Geometry  
  - math.NT — Number Theory  
  - math.NA — Numerical Analysis  
  - math.OA — Operator Algebras  
  - math.OC — Optimization and Control  
  - math.PR — Probability  
  - math.QA — Quantum Algebra  
  - math.RT — Representation Theory  
  - math.RA — Rings and Algebras  
  - math.SP — Spectral Theory  
  - math.ST — Statistics Theory  
  - math.SG — Symplectic Geometry  
## Computer Science (CoRR)

- **cs** — Computing Research Repository  
  - cs.AI — Artificial Intelligence  
  - cs.CL — Computation and Language  
  - cs.CC — Computational Complexity  
  - cs.CE — Computational Engineering, Finance, and Science  
  - cs.CG — Computational Geometry  
  - cs.GT — Computer Science and Game Theory  
  - cs.CV — Computer Vision and Pattern Recognition  
  - cs.CY — Computers and Society  
  - cs.CR — Cryptography and Security  
  - cs.DS — Data Structures and Algorithms  
  - cs.DB — Databases  
  - cs.DL — Digital Libraries  
  - cs.DM — Discrete Mathematics  
  - cs.DC — Distributed, Parallel, and Cluster Computing  
  - cs.ET — Emerging Technologies  
  - cs.FL — Formal Languages and Automata Theory  
  - cs.GL — General Literature  
  - cs.GR — Graphics  
  - cs.AR — Hardware Architecture  
  - cs.HC — Human-Computer Interaction  
  - cs.IR — Information Retrieval  
  - cs.IT — Information Theory  
  - cs.LO — Logic in Computer Science  
  - cs.LG — Machine Learning  
  - cs.MS — Mathematical Software  
  - cs.MA — Multiagent Systems  
  - cs.MM — Multimedia  
  - cs.NI — Networking and Internet Architecture  
  - cs.NE — Neural and Evolutionary Computing  
  - cs.NA — Numerical Analysis  
  - cs.OS — Operating Systems  
  - cs.OH — Other Computer Science  
  - cs.PF — Performance  
  - cs.PL — Programming Languages  
  - cs.RO — Robotics  
  - cs.SI — Social and Information Networks  
  - cs.SE — Software Engineering  
  - cs.SD — Sound  
  - cs.SC — Symbolic Computation  
  - cs.SY — Systems and Control  
## Quantitative Biology

- **q-bio** — Quantitative Biology  
