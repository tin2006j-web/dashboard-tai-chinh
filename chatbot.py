import pandas as pd
from database import load_data

def custom_chatbot(user_question):
    sales, customers = load_data()
    if sales is None or customers is None:
        return "⚠️ Trợ lý ảo chưa thể truy cập hệ thống dữ liệu!"
    question = user_question.lower()
    
    if "doanh thu" in question:
        return f"📊 **Doanh thu:** Tổng doanh thu hệ thống là **{sales['revenue'].sum():,.0f} VND**."
    elif "lợi nhuận" in question:
        return f"💰 **Lợi nhuận:** Tổng lợi nhuận ròng hiện tại đạt **{sales['profit'].sum():,.0f} VND**."
    elif "nợ lâu nhất" in question or "khách hàng nợ" in question:
        top_debtors = customers.sort_values(by='last_payment_days', ascending=False).head(3)
        res = "⚠️ **Khách hàng nợ lâu nhất:**\n\n"
        for _, row in top_debtors.iterrows():
            res += f"- **{row['customer_name']}**: Nợ *{row['debt']:,.0f} VND* ({row['last_payment_days']} ngày chưa trả).\n"
        return res
    elif "nguyên liệu tăng 10%" in question:
        current_profit = sales['profit'].sum()
        sim_cost = sales['quantity'] * sales['cost'] * 1.1
        sim_profit = sales['revenue'].sum() - sim_cost.sum()
        return f"📉 **Giả định:** Nếu nguyên liệu tăng **10%**, lợi nhuận sẽ giảm từ *{current_profit:,.0f} đ* xuống còn **{sim_profit:,.0f} đ**."
    else:
        return "🤖 Tôi hiểu câu hỏi về: `doanh thu`, `lợi nhuận`, `nợ lâu nhất`, và `nguyên liệu tăng 10%`."
