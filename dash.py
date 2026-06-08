import os
import streamlit as st

# Mẹo nhỏ: Cấu hình trang hiển thị dạng rộng để khi vào Canva không bị bóp nghẹt giao diện
st.set_page_config(layout="wide")
from pyngrok import ngrok

# ÉP HỆ THỐNG TẮT SẠCH CÁC KẾT NỐI CŨ ĐANG BỊ LỖI
try:
    ngrok.kill()
except:
    pass

# Tạo link mới kèm cấu hình tự động bỏ qua trang cảnh báo của Canva
try:
    config = {"request_header": {"add": ["ngrok-skip-browser-warning: true"]}}
    public_url = ngrok.connect(8501, config=config).public_url
    print("\n" + "="*50)
    print(f"🔗 LINK MỚI ĐỂ DÁN VÀO CANVA CỦA BẠN LÀ:\n{public_url}")
    print("="*50 + "\n")
except Exception as e:
    pass

# CHÈN ĐOẠN NÀY VÀO NGAY ĐẦU FILE DASH.PY
import os
from pyngrok import ngrok

# Tự động mở cổng ngrok khi chạy file
try:
    # Điền mã Authtoken của bạn vào đây nếu hệ thống yêu cầu
    # ngrok.set_auth_token("MÃ_AUTHTOKEN_CỦA_BẠN")
    
    config = {"request_header": {"add": ["ngrok-skip-browser-warning: true"]}}
    public_url = ngrok.connect(8501).public_url
    print("\n" + "="*50)
    print(f"🔗 LINK ĐỂ DÁN VÀO CANVA CỦA BẠN LÀ:\n{public_url}")
    print("="*50 + "\n")
except Exception as e:
    pass
import streamlit as st
import plotly.graph_objects as go

# 1. Cấu hình giao diện Dashboard
st.set_page_config(page_title="Phân Tích Giả Định", layout="centered")
st.title("📊 Phân Tích Giả Định & Tối Ưu Dây Chuyền")
st.caption("Di chuyển thanh trượt phía dưới để thay đổi số liệu kịch bản sản xuất")
st.markdown("---")

# 2. KHU VỰC CÁC THANH TRƯỢT ĐỘNG (SLIDERS)
st.subheader("⚙️ Thanh điều chỉnh thông số (What-If)")
col_sl1, col_sl2 = st.columns(2)

with col_sl1:
    st.markdown("**Bố trí nhân sự (Người):**")
    cd1_p = st.slider("Công đoạn 1 (Cắt giấy)", 1, 5, 2)
    cd4_p = st.slider("Công đoạn 4 (Gắn cờ)", 1, 5, 1)

with col_sl2:
    st.markdown("**Thời gian chu kỳ (Giây / SP):**")
    cd1_t = st.slider("Thời gian CĐ 1", 5, 30, 15)
    cd4_t = st.slider("Thời gian CĐ 4", 10, 60, 40)

# Các thông số mặc định khác của trò chơi
TOTAL_TIME = 240 # 4 phút
cd2_p, cd2_t = 1, 20
cd3_p, cd3_t = 1, 20
cd5_p, cd5_t = 1, 10

# 3. ENGINE TOÁN HỌC LOGISTICS TỰ ĐỘNG NHẢY SỐ
cap_cd1 = int((TOTAL_TIME / cd1_t) * cd1_p)
cap_cd2 = int((TOTAL_TIME / cd2_t) * cd2_p)
cap_cd3 = int((TOTAL_TIME / cd3_t) * cd3_p)
cap_cd4 = int((TOTAL_TIME / cd4_t) * cd4_p)
cap_cd5 = int((TOTAL_TIME / cd5_t) * cd5_p)

# Thành phẩm bị thắt nút bởi công đoạn thấp nhất (Bottleneck)
thanh_pham = min(cap_cd1, cap_cd2, cap_cd3, cap_cd4, cap_cd5)
hang_ton_wip = max(0, cap_cd1 - thanh_pham) + max(0, cap_cd2 - thanh_pham)
total_staff = cd1_p + cd2_p + cd3_p + cd4_p + cd5_p
nang_suat_ld = round(thanh_pham / total_staff, 2)

st.markdown("---")

# 4. HIỂN THỊ CÁC HỘP SỐ KẾT QUẢ ĐỘNG (SCORECARDS)
st.subheader("📈 Kết quả mô phỏng thời gian thực")
c1, c2, c3 = st.columns(3)
with c1:
    st.metric(label="🎁 Tổng thành phẩm", value=f"{thanh_pham} SP")
with c2:
    st.metric(label="📦 Hàng tồn trên chuyền (WIP)", value=f"{hang_ton_wip} SP")
with c3:
    st.metric(label="⚡ Năng suất lao động", value=f"{nang_suat_ld} SP/Người")

# 5. BIỂU ĐỒ NĂNG LỰC DÂY CHUYỀN
stages = ['CĐ 1: Cắt giấy', 'CĐ 2: Vòng đỏ', 'CĐ 3: Vòng vàng', 'CĐ 4: Gắn cờ', 'CĐ 5: Kiểm tra']
capacities = [cap_cd1, cap_cd2, cap_cd3, cap_cd4, cap_cd5]
colors = ['#31333F'] * 5
colors[capacities.index(min(capacities))] = '#FF4B4B' # Cột thấp nhất tự biến thành màu đỏ

fig = go.Figure(data=[go.Bar(x=stages, y=capacities, marker_color=colors, text=capacities, textposition='auto')])
fig.update_layout(yaxis_title="Sản lượng tối đa (SP)", template="plotly_white", height=300, margin=dict(l=10, r=10, t=10, b=10))
fig.add_hline(y=thanh_pham, line_dash="dash", line_color="#FF4B4B")
st.plotly_chart(fig, use_container_width=True)
