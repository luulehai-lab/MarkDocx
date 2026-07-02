# 🔬 Tài Liệu Kiểm Thử Khoa Học Phức Tạp (Science Test Suite)

Tài liệu này chứa các công thức toán học, vật lý, hóa học và sinh học có độ phức tạp cao nhằm kiểm tra hiệu năng render MathJax offline và bộ dịch xuất file PDF/Word.

---

## 📐 1. Toán Học Cao Cấp (Advanced Mathematics)

### 1.1 Tích phân đa lớp và Tích phân đường Cauchy
Định lý tích phân Cauchy cho một hàm giải tích trên miền đơn liên:

$$
\oint_{C} f(z) \, dz = 0
$$

Công thức tích phân Cauchy cho các đạo hàm cấp cao:

$$
f^{(n)}(z_0) = \frac{n!}{2\pi i} \oint_{C} \frac{f(z)}{(z-z_0)^{n+1}} \, dz
$$

### 1.2 Giới hạn và Chuỗi vô hạn (Infinite Series)
Biểu thức biểu diễn hằng số toán học $e$ và chuỗi Taylor của hàm số:

$$
e = \lim_{n \to \infty} \left(1 + \frac{1}{n}\right)^n = \sum_{k=0}^{\infty} \frac{1}{k!}
$$

Tổng Riemann đa chiều và Tích phân Gauss:

$$
\int_{-\infty}^{\infty} e^{-x^2} \, dx = \sqrt{\pi}
$$

### 1.3 Căn thức lồng nhau và Phân số liên tục (Nested Radicals & Continued Fractions)
Tỷ lệ vàng $\phi$ dưới dạng căn lồng nhau vô hạn và phân số liên tục:

$$
\phi = \sqrt{1 + \sqrt{1 + \sqrt{1 + \sqrt{1 + \dots}}}}
$$

$$
\phi = 1 + \frac{1}{1 + \frac{1}{1 + \frac{1}{1 + \frac{1}{1 + \dots}}}}
$$

### 1.4 Đại số tuyến tính và Ma trận (Linear Algebra & Matrices)
Ma trận xoay trong không gian 3D quay quanh trục $z$ góc $\theta$:

$$
R_z(\theta) = \begin{pmatrix}
\cos\theta & -\sin\theta & 0 \\
\sin\theta & \cos\theta & 0 \\
0 & 0 & 1
\end{pmatrix}
$$

Tính định thức và phương trình đặc trưng tìm trị riêng (Eigenvalues):

$$
\det(A - \lambda I) = 0
$$

---

## ⚡ 2. Vật Lý Lý Thuyết & Lượng Tử (Theoretical & Quantum Physics)

### 2.1 Phương trình trường Einstein (General Relativity)
Mô tả lực hấp dẫn dưới dạng độ cong không-thời gian trong thuyết tương đối rộng:

$$
G_{\mu\nu} + \Lambda g_{\mu\nu} = \frac{8\pi G}{c^4} T_{\mu\nu}
$$

### 2.2 Phương trình Schrödinger (Quantum Mechanics)
Phương trình Schrödinger phụ thuộc thời gian mô tả trạng thái lượng tử của một hệ vật lý:

$$
i\hbar \frac{\partial}{\partial t} \Psi(\mathbf{r}, t) = \left[ -\frac{\hbar^2}{2m} \nabla^2 + V(\mathbf{r}, t) \right] \Psi(\mathbf{r}, t)
$$

### 2.3 Hệ phương trình Maxwell (Electromagnetism)
Dạng vi phân của bốn phương trình Maxwell trong môi trường chân không:

$$
\nabla \cdot \mathbf{E} = \frac{\rho}{\varepsilon_0}
$$

$$
\nabla \cdot \mathbf{B} = 0
$$

$$
\nabla \times \mathbf{E} = -\frac{\partial \mathbf{B}}{\partial t}
$$

$$
\nabla \times \mathbf{B} = \mu_0 \mathbf{J} + \mu_0 \varepsilon_0 \frac{\partial \mathbf{E}}{\partial t}
$$

---

## 🧪 3. Hóa Học & Động Học Phản Ứng (Chemistry & Kinetics)

### 3.1 Cân bằng hóa học và Phương trình Nernst
Thế khử của điện cực phụ thuộc vào nồng độ các chất phản ứng ở nhiệt độ $T$:

$$
E = E^0 - \frac{RT}{nF} \ln Q
$$

Với $Q$ là hằng số cân bằng phản ứng:

$$
Q = \frac{[\text{C}]^c [\text{D}]^d}{[\text{A}]^a [\text{B}]^b}
$$

### 3.2 Động hóa học (Chemical Kinetics)
Phương trình Arrhenius biểu diễn sự phụ thuộc của hằng số tốc độ phản ứng $k$ vào nhiệt độ $T$:

$$
k = A e^{-\frac{E_a}{RT}}
$$

Phương trình phản ứng phân rã phóng xạ của hạt nhân cấp 1:

$$
N(t) = N_0 e^{-\lambda t}
$$

---

## 🧬 4. Sinh Học Định Lượng & Sinh Tin Học (Quantitative Biology)

### 4.1 Định luật di truyền Hardy-Weinberg
Mô tả tần số alen và kiểu gen trong một quần thể cân bằng di truyền:

$$
p^2 + 2pq + q^2 = 1
$$

Với $p + q = 1$, trong đó $p$ và $q$ lần lượt là tần số của hai alen khác nhau tại cùng một locus.

### 4.2 Hệ phương trình Lotka-Volterra (Mô hình Con mồi - Kẻ săn mồi)
Hệ phương trình vi phân mô tả sự biến động số lượng cá thể của con mồi $x$ và kẻ săn mồi $y$:

$$
\frac{dx}{dt} = \alpha x - \beta x y
$$

$$
\frac{dy}{dt} = \delta x y - \gamma y
$$

Hy vọng tài liệu này hiển thị xuất sắc trên trình xem của anh!
