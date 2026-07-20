# Tài liệu quy định về định dạng mã VietQR trong Dịch vụ Chuyển nhanh NAPAS247

> Nguồn: `na.pdf` — Công ty Cổ phần Thanh toán Quốc gia Việt Nam (NAPAS), Hà Nội, tháng 09/2021. Phiên bản 1.0.

## 1. Đối tượng áp dụng

Đối tượng áp dụng là các cá nhân/Tổ chức có nhu cầu sử dụng Tài liệu quy định dạng mã VietQR của NAPAS để chủ động xây dựng công cụ tạo mã VietQR sử dụng trong Dịch vụ Chuyển nhanh NAPAS247 nhằm thực hiện giao dịch Chuyển khoản bằng mã QR.

## 2. Phạm vi

Tài liệu này mô tả các quy định đối với định dạng mã VietQR sử dụng trong giao dịch chuyển khoản bằng mã QR thuộc Dịch vụ Chuyển nhanh NAPAS247.

## 3. Thuật ngữ và từ viết tắt

| STT | Thuật ngữ / từ viết tắt | Ý nghĩa |
|---|---|---|
| 1 | SW | Hệ thống chuyển mạch (Switch) của NAPAS |
| 2 | ACQ (NHTT) | Acquirer (Ngân hàng thanh toán) |
| 3 | ISS (NHPH) | Issuer (Ngân hàng phát hành) |
| 4 | BNB (NHTH) | Beneficiary Bank (Ngân hàng thụ hưởng) |
| 5 | TGTT | Trung gian thanh toán |
| 6 | NHTV | Ngân hàng thành viên |
| 7 | TCTV | Tổ chức thành viên (bao gồm NHTV và TGTT) |

## 4. Lịch sử thay đổi

| Ngày | Phiên bản | Thay đổi |
|---|---|---|
| 2021-09 | 1.0 | Phát hành bản đầu tiên |

## 5. Cấu trúc đối tượng dữ liệu

Đặc tả cấu trúc dữ liệu VietQR tuân theo Tiêu chuẩn cơ sở về QR của NHNH, tuân theo chuẩn QR code Merchant Presented của EMVCo.

### 5.1 Cấu trúc dữ liệu gốc

Dữ liệu chứa trong một mã QR được cấu trúc như sau, mỗi đối tượng dữ liệu được tạo thành 3 trường dữ liệu riêng lẻ. Trường đầu tiên là mô tả định danh (ID) mà đối tượng dữ liệu có thể được tham chiếu. Trường tiếp theo là trường chiều dài chỉ rõ số ký tự được thể hiện trong trường thứ ba. Một đối tượng dữ liệu sau đó được biểu diễn dưới dạng bao gồm ID/Chiều dài/Giá trị như sau:

- ID được mã hoá như là một giá trị số hai chữ số, với một giá trị khác nhau, từ "00" đến "99"
- Chiều dài được mã hoá dưới dạng một giá trị số hai chữ số, với giá trị từ "01" đến "99"
- Trường giá trị có độ dài tối thiểu là một ký tự và chiều dài tối đa là 99 ký tự

Đối tượng dữ liệu không được đóng gói trong một khuôn mẫu được cho là nằm dưới gốc của Mã QR.

Giá trị của một ID không phải là duy nhất và đối tượng dữ liệu mà nó đề cập là nội dung cụ thể. Nếu ID không nằm dưới gốc, bối cảnh của một ID được định nghĩa bởi mẫu đóng gói.

Ví dụ: ID "01" nằm dưới gốc của Mã QR đề cập đến Phương thức khởi tạo, trong khi ID "01" đề cập đến Số Hóa đơn khi nó nằm trong Mẫu Trường Dữ liệu Bổ sung (trong ID "62").

Định dạng Payload Format (ID "00") là đối tượng dữ liệu đầu tiên nằm dưới gốc và cho phép ứng dụng di động xác định dữ liệu đại diện của các dữ liệu còn lại có trong QR Code và cách phân tích dữ liệu. CRC (ID "63") là đối tượng dữ liệu cuối cùng nằm dưới gốc và cho phép ứng dụng di động kiểm tra tính toàn vẹn của dữ liệu được quét mà không cần phải phân tích tất cả các đối tượng dữ liệu. Vị trí của tất cả các đối tượng dữ liệu khác bên dưới gốc hoặc trong khuôn mẫu là tùy ý và có thể xuất hiện theo thứ tự bất kỳ.

Định dạng của trường giá trị trong một đối tượng dữ liệu là:

- **kiểu chữ số (N)**: các đối tượng dữ liệu có định dạng số [N] chỉ chứa các giá trị được biểu diễn bằng chữ số "0" đến "9". Mỗi chữ số được mã hóa trong mã QR bằng hệ nhị phân được định nghĩa theo quy định [Unicode].
- **ký tự đặc biệt (ANS)**: Ký tự đặc biệt chỉ chứa các giá trị được định nghĩa trong bộ ký tự chung của [EMV Book 4]. Mỗi ký tự mã hóa trong mã QR bằng hệ nhị phân được định nghĩa theo quy định [Unicode].
- **kiểu chuỗi (S)**: Chỉ chứa các giá trị có sẵn được định nghĩa bởi [Unicode]. Mỗi ký tự mã hóa trong mã QR bằng hệ nhị phân được định nghĩa theo quy định Unicode.

Lưu ý rằng kiểu số là một tập con của ký tự đặc biệt và ký tự đặc biệt là một tập con của Chuỗi.

Bảng 1 liệt kê tên của đối tượng dữ liệu, ID của đối tượng dữ liệu, định dạng trường giá trị của đối tượng dữ liệu, chiều dài trường giá trị của đối tượng dữ liệu, và sự hiện diện của đối tượng dữ liệu ở gốc cấp mã QR là bắt buộc (M), có điều kiện (C), hoặc không bắt buộc (O).

**Bảng 1 – Cấu trúc dữ liệu gốc của VietQR trong Dịch vụ Chuyển nhanh NAPAS247**

| Tên | ID | Định dạng | Độ dài | Hiển thị |
|---|---|---|---|---|
| Payload Format Indicator / Phiên bản dữ liệu | "00" | N | "02" | M |
| Point of Initiation Method / Phương thức khởi tạo | "01" | N | "02" | M |
| Merchant Account Information / Thông tin định danh ĐVCNTT | "38" | S | Tối đa "99" | M |
| Merchant Category Code / Mã danh mục ĐVCNTT | "52" | N | "04" | O |
| Transaction Currency / Mã tiền tệ | "53" | N | "03" | M |
| Transaction Amount / Số tiền GD | "54" | S | Tối đa "13" | C |
| Tip or Convenience Indicator / Chỉ thị cho Tip và Phí GD | "55" | N | "02" | O |
| Value of Convenience Fee Fixed / Giá trị phí cố định | "56" | S | Tối đa "13" | C |
| Value of Convenience Fee Percentage / Giá trị phí tỷ lệ phần trăm | "57" | S | Tối đa "05" | C |
| Country Code / Mã quốc gia | "58" | S | "02" | M |
| Merchant Name / Tên ĐVCNTT | "59" | ANS | Tối đa "25" ký tự | O |
| Merchant City / Thành phố của ĐVCNTT | "60" | ANS | Tối đa "15" | O |
| Postal Code / Mã bưu điện | "61" | ANS | Tối đa "10" | O |
| Additional Data Field Template / Thông tin bổ sung | "62" | ANS | Tối đa "99" | C |
| Merchant Information - Language Template / Thông tin ĐVCNTT khuôn mẫu Ngôn ngữ thay thế | "64" | ANS | Tối đa "99" | O |
| RFU for EMVCo / Đăng ký bởi EMVCo | "65"-"79" | ANS | Tối đa "99" | O |
| Unreserved Templates / Các thông tin bổ sung đăng ký dùng trong tương lai | "80"-"99" | ANS | Tối đa "99" | O |
| CRC (Cyclic Redundancy Check) | "63" | ANS | "04" | M |

Bảng 2 liệt kê tên của đối tượng dữ liệu, ID của đối tượng dữ liệu, định dạng trường giá trị của đối tượng dữ liệu, chiều dài trường giá trị của đối tượng dữ liệu, và dữ liệu sự hiện diện của đối tượng dữ liệu trong phần Bổ sung khuôn mẫu trường Dữ liệu (ID "62") của Mã QR là bắt buộc (M), có Điều kiện (C) hoặc Tùy chọn (O).

**Bảng 2 - Cấu trúc dữ liệu cho Thông tin bổ sung (ID "62") cho VietQR trong Dịch vụ Chuyển nhanh NAPAS247**

| Tên | ID | Định dạng | Độ dài | Hiển thị |
|---|---|---|---|---|
| Bill Number / Số hóa đơn | "01" | ANS | Tối đa "25" | C |
| Mobile Number / Số điện thoại di động | "02" | ANS | Tối đa "25" | C |
| Store Label / Mã cửa hàng | "03" | ANS | Tối đa "25" ký tự | O |
| Loyalty Number / Mã khách hàng thân thiết | "04" | ANS | Tối đa "25" | O |
| Reference Label / Mã tham chiếu | "05" | ANS | Tối đa "25" | C |
| Customer Label / Mã khách hàng | "06" | ANS | Tối đa "25" | C |
| Terminal Label / Mã số điểm bán hàng | "07" | ANS | Tối đa "25" | O |
| Purpose of Transaction / Mục đích giao dịch | "08" | ANS | Tối đa "25" | C |
| Additional Consumer Data Request / Yêu cầu dữ liệu KH bổ sung | "09" | ANS | Tối đa "03" | O |
| RFU for EMVCo / Đăng ký bởi EMVCo | "10"-"49" | ANS | — | O |
| Payment System specific templates / Hệ thống thanh toán cụ thể | "50"-"99" | ANS | — | O |

Mỗi đối tượng dữ liệu có ID "01" đến "08" trong Bảng 2 có thể được sử dụng theo hai cách: hoặc ĐVCNTT có thể cung cấp cả ID và giá trị có ý nghĩa của nó hoặc ĐVCNTT có thể bao gồm ID với một giá trị đặc biệt để có ứng dụng di động nhắc người tiêu dùng nhập thông tin này.

Để nhắc nhở người tiêu dùng về một hoặc nhiều giá trị này, ĐVCNTT sẽ bao gồm các ID tương ứng trong mỗi mẫu này với độ dài là "03" và có giá trị bằng "***".

Khi người tiêu dùng được nhắc nhở bởi ứng dụng di động để nhập một giá trị cho bất kỳ đối tượng dữ liệu nào, chiều dài của giá trị được nhập không được vượt quá chiều dài như được chỉ ra trong bảng 2.

Đối tượng dữ liệu có ID "09" chứa một hoặc nhiều giá trị cho biết ứng dụng di động dữ liệu cung cấp như một phần của yêu cầu bắt đầu giao dịch. Dữ liệu này đã được ứng dụng dành cho điện thoại di động biết đến và người dùng không cần phải nhắc nhở không cần thiết cho dữ liệu. Một hoặc nhiều ký tự sau đây có thể xuất hiện trong Dữ liệu người tiêu dùng Bổ sung Yêu cầu (ID "09") để chỉ ra rằng các dữ liệu tương ứng cần được cung cấp trong bắt đầu giao dịch để hoàn tất giao dịch:

- "A" = Địa chỉ của người tiêu dùng
- "M" = Số điện thoại di động của người tiêu dùng
- "E" = Địa chỉ email của người tiêu dùng

Nếu có nhiều hơn một ký tự, nó có nghĩa là mỗi đối tượng dữ liệu tương ứng được yêu cầu để hoàn tất giao dịch. Lưu ý rằng mỗi ký tự chỉ được xuất hiện duy nhất một lần.

Bảng 3 liệt kê tên của đối tượng dữ liệu, ID của đối tượng dữ liệu, định dạng trường giá trị của đối tượng dữ liệu, chiều dài trường giá trị của đối tượng dữ liệu và liệu sự hiện diện của đối tượng dữ liệu trong ngôn ngữ thông tin ĐVCNTT (ID "64") của Mã QR là Bắt buộc (M), có Điều kiện (C) hoặc Tùy chọn (O).

Những đối tượng dữ liệu này có thể được sử dụng bởi một ứng dụng di động để trình bày thông tin ĐVCNTT bằng một ngôn ngữ thay thế.

**Bảng 3 – Thông tin ĐVCNTT - Ngôn ngữ thay thế (ID "64")**

| Tên | ID | Định dạng | Độ dài | Hiển thị |
|---|---|---|---|---|
| Language Preference / Ngôn ngữ thay thế | "00" | ANS | "02" | M |
| Merchant Name - Alternate Language / Tên ĐVCNTT dưới dạng Ngôn ngữ thay thế | "01" | S | Tối đa "25" | M |
| Merchant City - Alternate Language / Thành phố dưới dạng ngôn ngữ thay thế | "02" | S | Tối đa "15" | O |
| RFU for EMVCo / Đăng ký bởi EMVCo | "03"-"99" | S | Tối đa "99" | — |

Các đối tượng dữ liệu có ID "01" và "02" được sử dụng như là một bổ sung cho thông tin ĐVCNTT dưới thư mục gốc. Trong khi các đối tượng dữ liệu tương đương dưới gốc được định nghĩa với định dạng Alphanumeric đặc biệt, và do đó chỉ có thể chứa bộ ký tự Thông thường, các đối tượng dữ liệu này, nếu có, được định nghĩa với một định dạng Chuỗi, do đó có thể chứa một bộ ký tự khác.

### 5.2 Đối tượng dữ liệu gốc

#### 5.2.1 Phiên bản dữ liệu (ID 00)

- Định dạng: N
- Độ dài: 2
- Hiển thị: Bắt buộc
- Ý nghĩa: Phiên bản dữ liệu là đối tượng dữ liệu đầu tiên trong mã QR, dùng để xác định phiên bản mã QR và các quy ước về ID, độ dài, giá trị. Phiên bản dữ liệu có giá trị là "01". Các giá trị khác được đăng ký dự phòng.

#### 5.2.2 Phương thức khởi tạo (ID 01)

- Định dạng: N
- Độ dài: 2
- Hiển thị: Bắt buộc
- Ý nghĩa: Phương thức khởi tạo xác định công nghệ giao tiếp và phân biệt dữ liệu là động hay tĩnh.
  - "11" = QR tĩnh – áp dụng khi mã QR cho phép thực hiện nhiều lần giao dịch.
  - "12" = QR động – áp dụng khi mã QR chỉ cho phép thực hiện một lần giao dịch.

#### 5.2.3 Thông tin định danh ĐVCNTT (ID 02-51)

- Định dạng: S
- Độ dài: tối đa 99
- Hiển thị: Bắt buộc
- Ý nghĩa: Thông tin định danh ĐVCNTT được sử dụng để định danh một ĐVCNTT cụ thể. Dịch vụ Chuyển nhanh NAPAS247 thông tin định danh khách hàng thụ hưởng và Ngân hàng thụ hưởng.

##### 5.2.3.1 Thông tin định danh ĐVCNTT ID 02-25

Các ID 02-25 được đăng ký bởi các tổ chức quốc tế, trong đó:

- ID 02-03: đăng ký bởi Tổ chức thẻ quốc tế Visa
- ID 04-05: đăng ký bởi Tổ chức thẻ quốc tế Mastercard
- ID 06-08: đăng ký bởi EMVCo
- ID 09-10: đăng ký bởi Tổ chức thẻ quốc tế Discover
- ID 11-12: đăng ký bởi Tổ chức thẻ quốc tế Amex
- ID 13-14: đăng ký bởi Tổ chức thẻ quốc tế JCB
- ID 15-16: đăng ký bởi Tổ chức thẻ quốc tế UnionPay
- ID 17-25: đăng ký bởi EMVCo

##### 5.2.3.2 Thông tin định danh ĐVCNTT ID 38

Các ID 26-51 được sử dụng cho các Trung gian thanh toán hoặc Ngân hàng khác nằm ngoài các Tổ chức thanh toán đã được liệt kê tại ID 02-25. ID 38 được sử dụng cho dịch vụ VietQR qua hệ thống Napas.

**Bảng 4 - Thành phần dữ liệu trường Thông tin tài khoản ĐVCNTT**

| Tên | ID | Định dạng | Độ dài | Hiển thị | Ghi chú |
|---|---|---|---|---|---|
| Định danh duy nhất toàn cầu - GUID | "00" | S | Tối đa "32" | M | ID quy định dữ liệu với 1 trong các giá trị sau: AID: luôn có giá trị "A000000727". |
| Tổ chức thụ hưởng (NHTV, TGTT) | "01" | S | — | M | Sự kết hợp của các đối tượng dữ liệu với các ID và loại đối tượng dữ liệu cụ thể đối với GUID. Sub tab "00": độ dài 6, định dạng S, ý nghĩa Acquirer ID/BNB ID. Sub tab "01": độ dài tối đa 19, định dạng S, ý nghĩa Merchant ID/Consumer ID. VD: `0006970403011621129950446040 25` → Sub tab 00 (độ dài 06) = `970403`; Sub tab 01 (độ dài 16) = `2112995044604025` |
| Mã dịch vụ | "02" | S | Tối đa "10" | C | - QRIBFTTC: dịch vụ chuyển nhanh NAPAS247 bằng mã QR đến thẻ. <br> - QRIBFTTA: dịch vụ chuyển nhanh NAPAS247 bằng mã QR đến Tài khoản. |

**5.2.3.2.1 Định danh duy nhất toàn cầu - GUID (ID 00):**

Có định dạng chữ số với độ dài tối đa 32 ký tự, cụ thể là AID của NAPAS: `A000000727`.

**5.2.3.2.2 Định danh ĐVCNTT (ID 01):**

Bao gồm 02 phần con như sau:

- Định danh ACQ ID/ BNB ID: các ngân hàng tại Việt Nam sử dụng mã BIN cấp bởi NHNN. VD: `970403`.
- Định danh Merchant ID/ Consumer ID có định dạng chữ số (ANS) với độ dài tối đa 19 ký tự. Giá trị của Merchant ID có thể là Mã số thuế, mã số doanh nghiệp, mã số đăng ký hộ kinh doanh hoặc mã định danh, chuỗi ký tự tùy chọn theo quy định cụ thể của ngân hàng thanh toán. Giá trị của Consumer ID là số tài khoản của khách hàng mở tại NH thụ hưởng (BNB ID).

**5.2.3.2.3 Mã dịch vụ (ID 02):**

| Giá trị | Ý nghĩa |
|---|---|
| QRIBFTTC | Mã dịch vụ chuyển tiền nhanh 24/7 bằng QR đến thẻ |
| QRIBFTTA | Mã dịch vụ chuyển tiền nhanh 24/7 bằng QR đến tài khoản |

**5.2.3.2.4 Ví dụ:**

VD: Dịch vụ Chuyển nhanh NAPAS247 bằng QR đến tài khoản

```
38570010A000000727012700069704 68011300110099504460208QRIBFTTA
```

| Tên | ID | Độ dài | Giá trị |
|---|---|---|---|
| Định danh duy nhất toàn cầu - GUID | 00 | 10 | A000000727 |
| Tổ chức thụ hưởng (NHTV, TGTT) | 01 | 27 | Sub tab 00 (độ dài 06) = `970468` (BNB ID); Sub tab 01 (độ dài 13) = `0011009950446` (Consumer ID) |
| Mã dịch vụ | 02 | 08 | QRIBFTTA |

#### 5.2.4 Mã danh mục ĐVCNTT (ID 52)

- Định dạng: N
- Độ dài: 4
- Hiển thị: không bắt buộc
- Ý nghĩa: Mã danh mục ĐVCNTT tuân theo chuẩn ISO 18245 và được ấn định bởi tổ chức thanh toán. MCC này phải chỉ ra Mã loại hàng hóa của người bán.

**Bảng 5 – Danh sách MCC**

| MCC | Ý nghĩa | Diễn giải |
|---|---|---|
| 5139 | Commercial Footwear | Giày dép |
| 5192 | Books, Periodicals, and Newspapers | Sách, ấn phẩm định kỳ và báo chí |
| 5231 | Glass, Paint, Wallpaper Stores | Kính, sơn và giấy dán tường |
| 5411 | Supermarkets, Grocery Stores | Siêu thị và Tạp hóa |
| 5611 | Men's and Boy's Clothing and Accessories Stores | Quần áo và phụ kiện cho Nam |
| 5621 | Women's Ready-to-Wear Stores | Hàng hiệu trang phục cho Nữ |
| 5631 | Women's Accessory and Specialty Shops | Phụ kiện cho Nữ |
| 5641 | Children's and Infant's Wear Stores | Quần áo trẻ em và trẻ sơ sinh |
| 5651 | Family Clothing Stores | Quần áo gia đình |
| 5661 | Shoe Stores | Giầy |
| 5691 | Men's and Women's Clothing Stores | Quần áo nam và nữ |
| 5734 | Computer Software Stores | Cửa hàng kinh doanh phần mềm máy tính |
| 5812 | Eating places and Restaurants | Địa điểm ăn uống và nhà hàng |
| 5813 | Drinking Places (Alcoholic Beverages), Bars, Taverns, Cocktail lounges, Nightclubs and Discotheques | Địa điểm uống (đồ uống có cồn), quán bar, quán rượu, câu lạc bộ đêm và vũ trường |
| 5814 | Fast Food Restaurants | Cửa hàng bán đồ ăn nhanh |
| 5912 | Drug Stores and Pharmacies | Cửa hàng thuốc và nhà thuốc |
| 5921 | Package Stores – Beer, Wine, and Liquor | Cửa hàng bia, rượu và đồ uống có cồn |
| 5832 | Antique Shops – Sales, Repairs, and Restoration Services | Đồ cổ, dịch vụ sửa chữa và phục hồi |
| 5940 | Bicycle Shops – Sales and Service | Cửa hàng xe đạp |
| 5941 | Sporting Goods Stores | Đồ thể thao |
| 5942 | Book Stores | Cửa hàng sách |
| 5943 | Stationery Stores, Office and School Supply Stores | Văn phòng phẩm và đồ dùng học tập |
| 5944 | Watch, Clock, Jewelry, and Silverware Stores | Đồng hồ, trang sức và đá quý |
| 5945 | Hobby, Toy, and Game Shops | Đồ chơi và trò chơi điện tử |
| 5946 | Camera and Photographic Supply Stores | Máy ảnh và phụ kiện nhiếp ảnh |
| 5947 | Card Shops, Gift, Novelty, and Souvenir Shops | Quà tặng và đồ lưu niệm |
| 5977 | Cosmetic Stores | Mỹ phẩm |
| 5992 | Florists | Cửa hàng Hoa |
| 5995 | Pet Shops, Pet Foods, and Supplies Stores | Thú cưng và thực phẩm thú cưng |
| 6011 | Financial Institutions – Manual Cash Disbursements | Tổ chức tài chính – rút tiền mặt |
| 7011 | Lodging – Hotels, Motels, Resorts, Central Reservation Services (not elsewhere classified) | Nhà nghỉ - khách sạn, khu nghỉ mát |
| 7211 | Laundry Services - Family and Commercial | Dịch vụ giặt ủi |
| 7216 | Dry Cleaners | Giặt khô |
| 7298 | Health and Beauty Shops | Cửa hàng chăm sóc sức khỏe và làm đẹp |
| 8062 | Hospitals | Bệnh viện |

#### 5.2.5 Mã tiền tệ (ID 53)

- Định dạng: N
- Độ dài: 3
- Hiển thị: Bắt buộc
- Ý nghĩa: Mã tiền tệ tuân theo tiêu chuẩn ISO 4217, chỉ định đơn vị tiền tệ của giao dịch mà khách hàng có thể nhận biết được thông qua ứng dụng di động mỗi khi số tiền giao dịch được hiển thị hoặc khi khách hàng nhập số tiền vào ứng dụng.

**Bảng 6 – Danh sách mã Tiền tệ**

| Mã tiền tệ | Giá trị | Ý nghĩa |
|---|---|---|
| JPY | 392 | Yên Japan |
| KRW | 410 | Won Korea |
| MYR | 458 | Ringgit Malaysia |
| CNY | 156 | Nhân dân tệ |
| IDR | 360 | Rupiah Indonesia |
| PHP | 608 | Peso Philippines |
| SGD | 702 | Dollar Singapore |
| THB | 764 | Baht Thailand |
| VND | 704 | Viet Nam |

VD: VND được thể hiện bằng giá trị "704".

#### 5.2.6 Số tiền giao dịch (ID 54)

- Định dạng: S
- Độ dài: tối đa 13
- Hiển thị: Tùy chọn có điều kiện
- Ý nghĩa:

Nếu xuất hiện, số tiền giao dịch sẽ được hiển thị cho khách hàng thông qua ứng dụng di động. Số tiền giao dịch có giá trị khác 0, chỉ bao gồm các số từ "0" đến "9" và có thể chứa một ký tự ".". Nếu số tiền bao gồm số thập phân, ký tự "." sẽ được sử dụng để tách phần thập phân khỏi số nguyên và ký tự "." có thể xuất hiện ngay cả khi không có phần thập phân.

Số lượng ký tự sau phần thập phân phải khớp với số mũ tiền tệ liên quan đến mã tiền tệ theo quy định tại ISO 4217.

Số tiền không được chứa bất kỳ ký tự nào khác (VD: không được sử dụng ký tự khoảng cách để tách hàng nghìn).

VD: Số tiền giao dịch hợp lệ: "50000", "50000."

Số tiền giao dịch không hợp lệ: "50 000"

Nếu số tiền giao dịch không được hiển thị sẵn trên ứng dụng di động thì khách hàng sẽ nhập số tiền.

#### 5.2.7 Chỉ thị cho Tip và phí giao dịch (ID 55)

- Định dạng: N
- Độ dài: 2
- Hiển thị: Không bắt buộc
- Ý nghĩa: Nếu xuất hiện, Chỉ số Tip và Phí giao dịch sẽ bao gồm 1 trong các giá trị: "01", "02" hoặc "03". Các giá trị khác được đăng ký dự phòng.
  - Giá trị "01": Khách hàng nhập tiền tip trên ứng dụng di động
  - Giá trị "02": ĐVCNTT thu phí cố định được quy định tại (ID "56")
  - Giá trị "03": ĐVCNTT thu phí tỷ lệ phần trăm được quy định tại (ID "57")

Nếu Số tiền giao dịch không xuất hiện trong mã QR thì Chỉ số Tip và Phí giao dịch vẫn có thể xuất hiện.

#### 5.2.8 Giá trị phí cố định (ID 56)

- Định dạng: S
- Độ dài: tối đa 13
- Hiển thị: Tùy chọn có điều kiện
- Ý nghĩa: Nếu Chỉ số Tip và Phí giao dịch xuất hiện trong (ID "55") có giá trị = 02 thì Giá trị phí cố định (ID "56") sẽ xuất hiện. Số tiền phí cố định sẽ được hiển thị cho khách hàng thông qua ứng dụng di động. Số tiền phí cố định có giá trị khác 0, chỉ bao gồm các số từ "0" đến "9" và có thể chứa một ký tự ".". Nếu số tiền bao gồm số thập phân, ký tự "." sẽ được sử dụng để tách phần thập phân khỏi số nguyên và ký tự "." có thể xuất hiện ngay cả khi không có phần thập phân.

Nếu ID "55" có giá trị khác 02 thì ID "56" sẽ không xuất hiện.

#### 5.2.9 Giá trị phí tỷ lệ phần trăm (ID 57)

- Định dạng: S
- Độ dài: tối đa 5
- Hiển thị: Tùy chọn có điều kiện
- Ý nghĩa:

Nếu Chỉ số Tip và Phí giao dịch (ID "55") có giá trị = 03 thì Giá trị phí tỷ lệ phần trăm (ID "57") sẽ xuất hiện và có giá trị từ "00.01" đến "99.99". Giá trị phí tỷ lệ phần trăm sẽ chỉ bao gồm các ký tự số từ "0" đến "9" và có thể bao gồm 1 ký tự "." để ngăn cách phần thập phân. Ký tự "." vẫn có thể xuất hiện ngay cả khi không có số thập phân.

Giá trị phí tỷ lệ phần trăm không được bao gồm bất kỳ ký tự nào khác. VD: ký tự "%" không được phép sử dụng.

Nếu ID "55" có giá trị khác 03 thì ID "57" sẽ không xuất hiện.

#### 5.2.10 Mã quốc gia (ID 58)

- Định dạng: S
- Độ dài: 2 ký tự
- Hiển thị: Bắt buộc
- Ý nghĩa: Xác định quốc gia mà ĐVCNTT thực hiện giao dịch. Mã quốc gia được quy định theo [ISO 3166-1 alpha 2]. Mã quốc gia có thể được hiển thị cho khách hàng thông qua ứng dụng di động trong quá trình xử lý giao dịch.

**Bảng 7 – Danh sách mã Quốc Gia**

| Mã Quốc Gia | Ý nghĩa |
|---|---|
| JP | Japan |
| KR | Korea |
| MY | Malaysia |
| RC | China |
| RI | Indonesia |
| RP | Philippines |
| SG | Singapore |
| TH | Thailand |
| VN | Viet Nam |

#### 5.2.11 Tên ĐVCNTT (ID 59)

- Định dạng: ANS
- Độ dài: tối đa 25
- Hiển thị: Không bắt buộc
- Ý nghĩa: Tên giao dịch của ĐVCNTT, có thể được hiển thị cho khách hàng thông qua ứng dụng di động trong quá trình xử lý giao dịch.

#### 5.2.12 Thành phố (ID 60)

- Định dạng: ANS
- Độ dài: tối đa 15
- Hiển thị: Không bắt buộc
- Ý nghĩa: Thành phố của ĐVCNTT chỉ định địa điểm vật lý mà ĐVCNTT hoạt động.

#### 5.2.13 Mã bưu điện (ID 61)

- Định dạng: ANS
- Độ dài: tối đa 10
- Hiển thị: Không bắt buộc
- Ý nghĩa: Nếu xuất hiện, mã bưu điện chỉ ra mã số bưu điện của nơi mà ĐVCNTT hoạt động. Tùy thuộc vào từng quốc gia, Mã bưu điện có thể là Zip code hoặc PIN code hoặc Postal code của ĐVCNTT.

#### 5.2.14 Thông tin bổ sung (ID 62)

- Định dạng: ANS
- Độ dài: tối đa 99 ký tự
- Hiển thị: Không bắt buộc
- Ý nghĩa: Trường Thông tin bổ sung cung cấp các dữ liệu bổ sung hỗ trợ trong các trường hợp khác nhau và bao gồm ít nhất 1 đối tượng dữ liệu.

**Bảng 8 - Dữ liệu Trường thông tin bổ sung**

| Tên | ID | Định dạng | Độ dài | Hiển thị | Mô tả |
|---|---|---|---|---|---|
| Bill Number / Số hóa đơn | "01" | ANS | Tối đa "25" | O | Số hóa đơn/biên lai cung cấp bởi Merchant hoặc do KH tự nhập vào app. |
| Mobile Number / Số điện thoại di động | "02" | ANS | Tối đa "25" | O | Số điện thoại di động có thể do merchant cung cấp hoặc do khách hàng tự nhập. |
| Store Label / Mã cửa hàng | "03" | ANS | Tối đa "25" | O | Giá trị đặc biệt gắn với một cửa hàng. Giá trị này có thể do merchant cung cấp hoặc do khách hàng tự nhập. |
| Loyalty Number / Mã khách hàng thân thiết | "04" | ANS | Tối đa "25" | O | Thông thường là số thẻ khách hàng thân thiết. Số này có thể do merchant cung cấp hoặc có thể khách hàng phải nhập Số thẻ khách hàng thân thiết của họ. |
| Reference Label / Mã tham chiếu | "05" | ANS | Tối đa "25" | O | Bất kì giá trị theo quy định bởi ĐVCNTT/Tổ chức thanh toán nhằm xác định GD. |
| Customer Label / Mã khách hàng | "06" | ANS | Tối đa "25" | O | Có thể là mã khách hàng, SĐT khách hàng, số hóa đơn... |
| Terminal Label / Mã số điểm bán | "07" | ANS | Tối đa "25" | O | Mã số riêng biệt liên quan đến thiết bị đầu cuối của cửa hàng. |
| Purpose of Transaction / Mục đích giao dịch | "08" | ANS | Tối đa "25" | O | Giá trị nhằm xác định mục đích của giao dịch, VD: nạp tiền điện thoại, mua hàng hóa… |
| Additional Consumer Data Request / Yêu cầu dữ liệu KH bổ sung | "09" | ANS | Tối đa "03" ký tự | O | Một hoặc nhiều ký tự sau đây có thể xuất hiện, cho biết dữ liệu tương ứng cần được cung cấp trong quá trình khởi tạo giao dịch: "A" = Địa chỉ khách hàng; "M" = SĐT khách hàng; "E" = Địa chỉ email của khách hàng |
| RFU for EMVCo / Đăng ký bởi EMVCo | "10"-"49" | S | — | O | Được đăng ký bởi EMVCo cho mục đích sử dụng trong tương lai |
| Payment System specific templates / Hệ thống thanh toán cụ thể | "50"-"99" | S | — | O | Được đăng ký bởi các hệ thống thanh toán cho mục đích sử dụng trong tương lai |

- Nếu xuất hiện, trường Thông tin bổ sung (ID 62) sẽ bao gồm ít nhất một đối tượng dữ liệu và tổng độ dài của tất cả các đối tượng dữ liệu trong ID 62 không vượt quá 99 ký tự.
- Nội dung của giá trị đối tượng cho các ID từ "01" đến "08" có thể là "***" hoặc là một giá trị do ĐVCNTT quy định. Nếu nội dung là "***" thì khách hàng sẽ nhập thông tin vào ứng dụng di động.
- Yêu cầu thông tin khách hàng bổ sung (ID "09") bao gồm bất kỳ sự kết hợp nào của các ký tự: "A", "M" và/hoặc "E", và sẽ chỉ có một giá trị duy nhất cho mỗi ký tự này.
- Nếu Hệ thống thanh toán cụ thể (ID 50-99) xuất hiện thì nó sẽ bao gồm GUID cơ bản (ID 00) với một trong các giá trị sau:
  - Một AID bao gồm một mã RID quy định theo ISO/IEC 7816-5, và có thể bao gồm một mã PIX theo ISO 7816-4. VD: "A000000727".
  - Một UUID không có dấu (-) ngăn cách. VD: "581b314e257f41bfbbdc6384daa31d16".
  - Một tên miền ngược. VD: "vn.com.napas.qrcodeservice".

#### 5.2.15 Mã kiểm thử giá trị - CRC (ID 63)

- Định dạng: ANS
- Độ dài: tối đa 4
- Hiển thị: Bắt buộc
- Ý nghĩa: CRC - Checksum được tính theo ISO/IEC 13239 bằng cách sử dụng đa thức '1021' (hex) và giá trị ban đầu 'FFFF' (hex). Checksum được tính cho tất cả các đối tượng dữ liệu, bao gồm ID, Độ dài và Giá trị nằm trong mã QR theo đúng thứ tự xuất hiện, ngoài ra bao gồm cả ID và Chiều dài của CRC (nhưng không bao gồm Giá trị của CRC). Cách tạo CRC xem chi tiết ở Mục 6.

#### 5.2.16 Thông tin ĐVCNTT – Ngôn ngữ thay thế (ID 64)

- Định dạng: ANS
- Độ dài: tối đa 99
- Hiển thị: Không bắt buộc
- Ý nghĩa: Thông tin ngôn ngữ ĐVCNTT – Ngôn ngữ thay thế bao gồm các thông tin ĐVCNTT bằng một ngôn ngữ thay thế và có thể sử dụng một bộ ký tự khác với Bộ ký tự chung.

**Bảng 9 - Thông tin ĐVCNTT – Trường ngôn ngữ thay thế**

| Tên | ID | Định dạng | Độ dài | Hiển thị |
|---|---|---|---|---|
| Language Preference / Ngôn ngữ thay thế | "00" | ANS | "02" | M |
| Merchant Name - Alternate Language / Tên ĐVCNTT dưới dạng ngôn ngữ thay thế | "01" | S | Tối đa "25" | M |
| Merchant City - Alternate Language / Thành phố dưới dạng ngôn ngữ thay thế | "02" | S | Tối đa "15" | O |
| RFU for EMVCo / Đăng ký bởi EMVCo | "03"-"99" | S | Tối đa "99" | — |

##### 5.2.16.1 Ngôn ngữ thay thế (ID 00)

- Định dạng: ANS
- Độ dài: 2
- Hiển thị: Bắt buộc
- Ý nghĩa: Ngôn ngữ thay thế được quy định bởi [ISO 639]. Giá trị này đại diện cho ngôn ngữ được sử dụng để mã hóa Tên ĐVCNTT dưới dạng ngôn ngữ thay thế và Tên thành phố dưới dạng ngôn ngữ thay thế.

##### 5.2.16.2 Tên ĐVCNTT dưới dạng ngôn ngữ thay thế (ID 01)

- Định dạng: S
- Độ dài: tối đa 25
- Hiển thị: Bắt buộc
- Ý nghĩa: Tên giao dịch của ĐVCNTT bằng ngôn ngữ bản địa của ĐVCNTT đó.

##### 5.2.16.3 Thành phố dưới dạng Ngôn ngữ thay thế (ID 02)

- Định dạng: S
- Độ dài: tối đa 15 ký tự
- Hiển thị: Không bắt buộc
- Ý nghĩa: Tên thành phố của ĐVCNTT bằng ngôn ngữ bản địa của ĐVCNTT đó.

#### 5.2.17 Đăng ký bởi EMVCo (ID 65-79)

- Định dạng: ANS
- Độ dài: tối đa 99
- Hiển thị: Không bắt buộc
- Ý nghĩa: Các đối tượng dữ liệu đã được đăng ký bởi EMVCo cho mục đích sử dụng trong tương lai.

#### 5.2.18 Thông tin bổ sung đăng ký dùng trong tương lai (ID 80-99)

- Định dạng: ANS
- Độ dài: tối đa 99
- Hiển thị: Không bắt buộc
- Ý nghĩa:
  - Mã QR có thể không chứa hoặc chứa nhiều Thông tin bổ sung.
  - Thông tin bổ sung chưa được đăng ký có thể được phân bổ và sử dụng bởi các bên khác, như các hệ thống thanh toán (nội địa) và các nhà cung cấp dịch vụ giá trị gia tăng sử dụng cho sản phẩm của riêng họ. Sau đó, họ có thể xác định ý nghĩa, mô tả và định dạng cho mã QR. Mỗi nhà cung cấp hệ thống thanh toán hoặc dịch vụ giá trị gia tăng quy định dữ liệu của họ vào một ID riêng biệt của Thông tin bổ sung. Ví dụ, bộ dữ liệu đầu tiên được quy định trong ID "80", bộ dữ liệu thứ hai được quy định trong ID "81", vv.

**Bảng 10 - Trường thông tin bổ sung đăng ký dùng trong tương lai**

| Tên | ID | Định dạng | Độ dài | Hiển thị | Ghi chú |
|---|---|---|---|---|---|
| Globally Unique Identifier - GUID / Định danh duy nhất toàn cầu | "00" | ANS | Tối đa "32" ký tự | Bắt buộc | ID quy định dữ liệu với 1 trong các giá trị sau: AID; UUID không có dấu (-) ngăn cách; Tên miền ngược. |
| Context specific data / Dữ liệu phạm vi cụ thể | "01"-"99" | S | — | Không bắt buộc | Sự kết hợp của các đối tượng dữ liệu với các ID và loại đối tượng dữ liệu cụ thể đối với GUID. |

Nếu xuất hiện, Thông tin bổ sung chứa các thành phần dữ liệu sau:

- GUID (ID "00") bao gồm một trong các giá trị:
  - Một AID bao gồm một mã RID quy định theo ISO/IEC 7816-5, và có thể bao gồm một mã PIX theo ISO 7816-4. VD: "A000000727".
  - Một UUID không có dấu (-) ngăn cách. VD: "581b314e257f41bfbbdc6384daa31d16".
  - Một tên miền ngược. Ví dụ, "vn.com.napas.qrcodeservice".
- Dữ liệu phạm vi cụ thể (ID "01" – "99"): Sự kết hợp của các đối tượng dữ liệu với các ID và loại đối tượng dữ liệu cụ thể đối với GUID.

## 6. Diễn tả QR code

### 6.1 Mã QR sử dụng trong Dịch vụ Chuyển nhanh NAPAS247

#### 6.1.1 QR tĩnh đến tài khoản

```
00020101021138570010A00000072701270006970403011200110123456780208QRIBFTTA53037045802VN6304F4E5
```

| Tên | ID | Độ dài | Giá trị |
|---|---|---|---|
| Payload Format Indicator / Phiên bản dữ liệu | 00 | 02 | 01 |
| Point of Initiation Method / Phương thức khởi tạo | 01 | 02 | 11 |
| Consumer Account Information / Thông tin định danh người thụ hưởng | 38 | 57 | `0010A000000727012700069704030113001101234567 80208QRIBFTTA` |
| Transaction Currency / Mã tiền tệ | 53 | 03 | 704 |
| Country Code / Mã quốc gia | 58 | 02 | VN |
| CRC (Cyclic Redundancy Check) | 63 | 04 | F4E5 |

Các bước thực hiện Tạo QR:

| Bước thực hiện | Dữ liệu đầu vào | Kết quả mong đợi |
|---|---|---|
| Tạo CRC ([lammertbies.nl CRC calculator](http://www.lammertbies.nl/comm/info/crc-calculation.html)) | `000201010211385700 10A000000727012700069704030112 00110123456780208QRIBFTTA5303 70458 02VN6304` | F4E5 |
| Tạo Mã QR ([the-qrcode-generator.com](https://www.the-qrcode-generator.com/)) | `000201010211385700 10A000000727012700069704030112 00110123456780208QRIBFTTA5303 70458 02VN6304F4E5` | (ảnh QR code) |

#### 6.1.2 QR tĩnh đến thẻ

```
00020101021138600010A00000072701300006970403011697040311012345670208QRIBFTTC53037045802VN63044F52
```

| Tên | ID | Độ dài | Giá trị |
|---|---|---|---|
| Payload Format Indicator / Phiên bản dữ liệu | 00 | 02 | 01 |
| Point of Initiation Method / Phương thức khởi tạo | 01 | 02 | 11 |
| Consumer Account Information / Thông tin định danh người thụ hưởng | 38 | 60 | `0010A00000072701300006970403011 6970403110123456 70208QRIBFTTC` |
| Transaction Currency / Mã tiền tệ | 53 | 03 | 704 |
| Country Code / Mã quốc gia | 58 | 02 | VN |
| CRC (Cyclic Redundancy Check) | 63 | 04 | 4F52 |

Các bước thực hiện Tạo QR:

| Bước thực hiện | Dữ liệu đầu vào | Kết quả mong đợi |
|---|---|---|
| Tạo CRC | `000201010211386000 10A000000727013000069704030116 97040311012345670208QRIBFTTC53 037045802VN6304` | 4F52 |
| Tạo Mã QR | `000201010211386000 10A000000727013000069704030116 97040311012345670208QRIBFTTC53 037045802VN63044F52` | (ảnh QR code) |

#### 6.1.3 QR động đến tài khoản

```
00020101021238570010A00000072701270006970403011300110123456780208QRIBFTTA530370454061800005802VN62340107NPS68690819thanh toan don hang63042E2E
```

| Tên | ID | Độ dài | Giá trị |
|---|---|---|---|
| Payload Format Indicator / Phiên bản dữ liệu | 00 | 02 | 01 |
| Point of Initiation Method / Phương thức khởi tạo | 01 | 02 | 12 |
| Consumer Account Information / Thông tin định danh người thụ hưởng | 38 | 57 | `0010A000000727012700069704030113001101234567 80208QRIBFTTA` |
| Transaction Currency / Mã tiền tệ | 53 | 03 | 704 |
| Transaction Amount / Số tiền GD | 54 | 06 | 180000 |
| Country Code / Mã quốc gia | 58 | 02 | VN |
| Additional Data Field Template / Thông tin bổ sung | 62 | 34 | `0107NPS6869 0819thanh toan don hang` |
| CRC (Cyclic Redundancy Check) | 63 | 04 | 2E2E |

Các bước thực hiện Tạo QR:

| Bước thực hiện | Dữ liệu đầu vào | Kết quả mong đợi |
|---|---|---|
| Tạo CRC | `00020101021238570010A00000072701270006970403011300110123456780208QRIBFTTA530370454061800005802VN62340107NPS68690819thanh toan don hang6304` | 2E2E |
| Tạo Mã QR | `00020101021238570010A00000072701270006970403011300110123456780208QRIBFTTA530370454061800005802VN62340107NPS68690819thanh toan don hang63042E2E` | (ảnh QR code) |

#### 6.1.4 QR động đến thẻ

```
00020101021238600010A00000072701300006970403011697040311012345670208QRIBFTTC530370454061800005802VN62340107NPS68690819thanh toan don hang6304A203
```

| Tên | ID | Độ dài | Giá trị |
|---|---|---|---|
| Payload Format Indicator / Phiên bản dữ liệu | 00 | 02 | 01 |
| Point of Initiation Method / Phương thức khởi tạo | 01 | 02 | 12 |
| Consumer Account Information / Thông tin định danh người thụ hưởng | 38 | 60 | `0010A00000072701300006970403011 6970403110123456 70208QRIBFTTC` |
| Transaction Currency / Mã tiền tệ | 53 | 03 | 704 |
| Transaction Amount / Số tiền GD | 54 | 06 | 180000 |
| Country Code / Mã quốc gia | 58 | 02 | VN |
| Additional Data Field Template / Thông tin bổ sung | 62 | 34 | `0107NPS6869 0819thanh toan don hang` |
| CRC (Cyclic Redundancy Check) | 63 | 04 | A203 |

Các bước thực hiện Tạo QR:

| Bước thực hiện | Dữ liệu đầu vào | Kết quả mong đợi |
|---|---|---|
| Tạo CRC | `00020101021238600010A00000072701300006970403011697040311012345670208QRIBFTTC530370454061800005802VN62340107NPS68690819thanh toan don hang6304` | A203 |
| Tạo Mã QR | `00020101021238600010A00000072701300006970403011697040311012345670208QRIBFTTC530370454061800005802VN62340107NPS68690819thanh toan don hang6304A203` | (ảnh QR code) |

## 7. Hiệu lực văn bản

Bộ Tiêu chuẩn kỹ thuật này có hiệu lực 2021.

## 8. Điều kiện và điều khoản sử dụng Tài liệu quy định về định dạng mã VietQR trong Dịch vụ chuyển tiền nhanh NAPAS247

Khi thực hiện tải, lưu trữ hoặc sử dụng Tài liệu quy định về định dạng mã VietQR của Dịch vụ Chuyển nhanh NAPAS247 trên website VietQR.net, Khách hàng được coi như đã đọc, chấp nhận và đồng ý chịu ràng buộc và cam kết tuân thủ các Điều khoản sử dụng dưới đây.

### 8.1 Giải thích từ ngữ

Trong phạm vi Điều kiện và điều khoản này, các từ ngữ dưới đây được hiểu như sau:

1. **Dịch vụ Chuyển nhanh NAPAS247** ("NAPAS247"): Là dịch vụ cho phép cá nhân/doanh nghiệp chuyển tiền từ tài khoản của mình tới một tài khoản tại một ngân hàng khác trong mạng lưới của NAPAS theo phương thức chuyển tiền nhanh 24/7 (thực hiện theo thời gian thực, 24 giờ/ngày, 7 ngày/tuần). Hạn mức tối đa của một giao dịch là dưới 500 triệu đồng.
2. **Khách hàng**: Là cá nhân/doanh nghiệp có nhu cầu sử dụng tài liệu quy định về định dạng mã VietQR trong Dịch vụ Chuyển nhanh NAPAS247.
3. **Mã QR/QR Code (Mã phản hồi nhanh) thanh toán**: Là thông tin thanh toán được mã hóa gồm: Số tài khoản, Mã hiệu ngân hàng, Số tiền, Nội dung thanh toán, Thông tin đơn hàng và các thông tin liên quan khác (nếu có) giúp việc khởi tạo lệnh thanh toán được thực hiện chính xác, nhanh chóng và an toàn. Mã QR trong thanh toán tuân thủ theo tiêu chuẩn thanh toán QR của EMV Co. và Tiêu chuẩn cơ sở cho mã QR do Ngân hàng Nhà nước Việt Nam ban hành.
4. **Chuyển khoản bằng mã QR**: Là phương thức chuyển tiền giữa các tài khoản ngân hàng thông qua hình thức quét mã QR.
5. **VietQR**: Là nhận diện thương hiệu dành cho các dịch vụ thanh toán, chuyển khoản bằng mã QR được xử lý qua mạng lưới NAPAS, các Ngân hàng thành viên, Trung gian thanh toán, các đối tác thanh toán tại Việt Nam và quốc tế của NAPAS.
6. **Mã VietQR**: Là mã QR được tạo theo quy định về định dạng mã QR của NAPAS sử dụng trong các dịch vụ VietQR.
7. **Tài liệu quy định về định dạng mã VietQR của Dịch vụ Chuyển nhanh NAPAS247** ("Tài liệu"): Là tài liệu do NAPAS ban hành và thuộc sở hữu của NAPAS, quy định chuẩn định dạng mã QR sử dụng trong Dịch vụ Chuyển nhanh NAPAS 247.

### 8.2 Phạm vi sử dụng tài liệu

Khách hàng tải và sử dụng Tài liệu để chủ động xây dựng công cụ tạo mã VietQR để thực hiện giao dịch Chuyển khoản bằng mã QR trong Dịch vụ Chuyển nhanh NAPAS247.

### 8.3 Quyền và trách nhiệm của Khách hàng

1. Được quyền xem, tải về, sử dụng miễn phí Tài liệu để xây dựng công cụ tạo mã VietQR trong Dịch vụ Chuyển nhanh NAPAS247 theo chuẩn định dạng của NAPAS.
2. Đồng ý, hiểu và nhận thức rõ rằng Tài liệu này thuộc toàn quyền sở hữu của NAPAS và trong mọi trường hợp cam kết:
   a) Không can thiệp hoặc nỗ lực thay đổi bất kỳ nội dung, cấu phần nào của Tài liệu dưới bất kỳ hình thức nào.
   b) Không sao chép, mua bán đối với một phần hoặc toàn bộ các nội dung trong Tài liệu, sử dụng Tài liệu không đúng mục đích quy định tại Mục II khi chưa có sự đồng ý bằng văn bản của NAPAS hoặc cho bất kỳ mục đích hoặc hoạt động phi pháp nào.
   c) Không có bất kỳ hành động nào thể hiện hoặc ngầm ý rằng Tài liệu này thuộc quyền sở hữu của Khách hàng.
3. Chịu hoàn toàn trách nhiệm và cam kết miễn trách cho NAPAS đối với bất kỳ thiệt hại, tổn thất, khiếu nại phát sinh liên quan đến việc chia sẻ, sử dụng và lưu trữ Tài liệu không chính xác, đầy đủ hoặc không phù hợp với quy định của NAPAS.
4. Chịu hoàn toàn trách nhiệm đối với các hoạt động kinh doanh của Khách hàng có sử dụng mã VietQR được tạo theo quy định về định dạng mã VietQR tại Tài liệu.
5. Chịu hoàn toàn trách nhiệm đối với việc quản lý và bảo mật thông tin thanh toán được mã hóa trong mã VietQR tạo bởi Khách hàng, bao gồm các thông tin về Số tài khoản, Mã hiệu ngân hàng, Số tiền, Nội dung thanh toán, Thông tin đơn hàng và các thông tin liên quan khác (nếu có).

### 8.4 Quyền sở hữu trí tuệ

1. Khách hàng đồng ý rằng Khách hàng không có quyền, yêu cầu hay lợi ích nào liên quan tới bất kỳ bản quyền, sáng chế, nhãn hiệu thương mại, tiêu chuẩn dịch vụ, tài sản, bí mật kinh doanh liên quan tới Tài liệu.
2. Khách hàng đồng ý không đưa ra bất kỳ tuyên bố hoặc có bất kỳ hành động nào nhằm xác lập hoặc thực hiện quyền hay yêu cầu đối với Tài liệu này.
