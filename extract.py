import os
import re
import csv
import glob

def extract_table_data(html_content):
    """
    使用正则表达式提取HTML表格中的数据
    支持单行或多行HTML表格数据
    """
    # 首先尝试提取表格行
    rows = re.findall(r'<tr[^>]*>(.*?)</tr>', html_content, re.DOTALL)
    data = []
    
    if rows:
        # 如果找到了多个表格行，则分别处理每一行
        for row in rows:
            cells = re.findall(r'<td[^>]*>(.*?)</td>', row)
            cleaned_cells = [re.sub(r'<[^>]+>', '', cell).strip() for cell in cells]
            if cleaned_cells:  # 确保行不为空
                data.append(cleaned_cells)
    else:
        # 如果没找到表格行标签，则尝试直接提取单元格（兼容旧格式）
        cells = re.findall(r'<td[^>]*>(.*?)</td>', html_content)
        cleaned_cells = [re.sub(r'<[^>]+>', '', cell).strip() for cell in cells]
        if cleaned_cells:
            data.append(cleaned_cells)
    
    return data

def process_file(input_file, output_file=None):
    """
    处理单个文件并将其转换为CSV
    """
    # 如果没有指定输出文件，则使用与输入文件相同的名称，但后缀为.csv
    if output_file is None:
        output_file = os.path.splitext(input_file)[0] + '.csv'
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 使用正则表达式解析表格数据
        data = extract_table_data(content)
        
        # 如果没有数据，返回错误消息
        if not data:
            return f"错误：在文件 {input_file} 中未找到表格数据"
        
        # 添加表头
        headers = ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"]
        
        # 写入CSV文件
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(data)
        
        return f"成功：已将 {input_file} 转换为 {output_file}"
    
    except Exception as e:
        return f"错误：处理文件 {input_file} 时出错 - {str(e)}"

def main():
    """
    主函数：处理目录中的所有txt文件
    """
    # 获取当前目录下所有的txt文件
    txt_files = glob.glob("*.txt")
    
    if not txt_files:
        print("错误：未找到txt文件")
        return
    
    print(f"找到 {len(txt_files)} 个txt文件需要处理")
    
    for txt_file in txt_files:
        result = process_file(txt_file)
        print(result)
    
    print("所有文件处理完成")

if __name__ == "__main__":
    main()
