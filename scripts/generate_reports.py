#!/usr/bin/env python3
"""
測試報告生成腳本
自動生成 Behave 和 Pytest 的 HTML 報告
"""

import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path

# 添加專案根目錄到 Python 路徑
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def ensure_reports_dir():
    """確保 reports 目錄存在"""
    reports_dir = project_root / "reports"
    reports_dir.mkdir(exist_ok=True)
    return reports_dir

def install_dependencies():
    """安裝必要的依賴"""
    print("📦 檢查並安裝依賴...")
    
    try:
        # 檢查 requirements.txt 是否存在
        requirements_file = project_root / "requirements.txt"
        if not requirements_file.exists():
            print("⚠️  找不到 requirements.txt 文件")
            return False
        
        # 安裝依賴
        cmd = ["pip", "install", "-r", str(requirements_file)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 依賴安裝成功")
            return True
        else:
            print(f"❌ 依賴安裝失敗: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("❌ 找不到 pip 命令")
        return False

def run_behave_report():
    """生成 Behave HTML 報告"""
    print("🔄 生成 Behave HTML 報告...")
    
    reports_dir = ensure_reports_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = reports_dir / f"behave-report_{timestamp}.html"
    
    try:
        cmd = [
            "behave",
            "--format=html-pretty",
            f"--outfile={report_file}",
            "--tags=~wip"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Behave 報告已生成: {report_file}")
            return str(report_file)
        else:
            print(f"❌ Behave 報告生成失敗: {result.stderr}")
            return None
            
    except FileNotFoundError:
        print("❌ 找不到 behave 命令，請確保已安裝 behave")
        return None

def run_pytest_report():
    """生成 Pytest HTML 報告"""
    print("🔄 生成 Pytest HTML 報告...")
    
    reports_dir = ensure_reports_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = reports_dir / f"pytest-report_{timestamp}.html"
    
    try:
        # 檢查是否有 pytest-html 插件
        check_cmd = ["python", "-m", "pytest", "--help"]
        result = subprocess.run(check_cmd, capture_output=True, text=True)
        
        if "--html" not in result.stdout:
            print("⚠️  Pytest HTML 插件未安裝，跳過 HTML 報告生成")
            print("💡 請運行: pip install pytest-html")
            return None
        
        cmd = [
            "python", "-m", "pytest",
            "--html", str(report_file),
            "--self-contained-html",
            "tests/",
            "-v"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Pytest 報告已生成: {report_file}")
            return str(report_file)
        else:
            print(f"❌ Pytest 報告生成失敗: {result.stderr}")
            return None
            
    except FileNotFoundError:
        print("❌ 找不到 pytest 命令，請確保已安裝 pytest")
        return None

def run_coverage_report():
    """生成覆蓋率報告"""
    print("🔄 生成覆蓋率報告...")
    
    reports_dir = ensure_reports_dir()
    coverage_dir = reports_dir / "coverage"
    
    try:
        # 檢查是否有 pytest-cov 插件
        check_cmd = ["python", "-m", "pytest", "--help"]
        result = subprocess.run(check_cmd, capture_output=True, text=True)
        
        if "--cov" not in result.stdout:
            print("⚠️  Pytest Coverage 插件未安裝，跳過覆蓋率報告生成")
            print("💡 請運行: pip install pytest-cov")
            return None
        
        cmd = [
            "python", "-m", "pytest",
            "--cov=src",
            f"--cov-report=html:{coverage_dir}",
            "--cov-report=term-missing",
            "tests/"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ 覆蓋率報告已生成: {coverage_dir}")
            return str(coverage_dir)
        else:
            print(f"❌ 覆蓋率報告生成失敗: {result.stderr}")
            return None
            
    except FileNotFoundError:
        print("❌ 找不到 pytest 命令，請確保已安裝 pytest-cov")
        return None

def cleanup_old_reports(keep_count=5):
    """清理舊的報告文件，只保留最新的幾個"""
    print("🧹 清理舊的報告文件...")
    
    reports_dir = ensure_reports_dir()
    
    # 清理 HTML 報告
    html_files = list(reports_dir.glob("*.html"))
    html_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    
    for old_file in html_files[keep_count:]:
        try:
            old_file.unlink()
            print(f"🗑️  已刪除: {old_file.name}")
        except Exception as e:
            print(f"⚠️  無法刪除 {old_file.name}: {e}")
    
    # 清理日誌文件
    log_files = list(reports_dir.glob("*.log"))
    log_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    
    for old_file in log_files[keep_count:]:
        try:
            old_file.unlink()
            print(f"🗑️  已刪除: {old_file.name}")
        except Exception as e:
            print(f"⚠️  無法刪除 {old_file.name}: {e}")

def main():
    """主函數"""
    print("🚀 開始生成測試報告...")
    print(f"📁 專案根目錄: {project_root}")
    
    # 確保 reports 目錄存在
    ensure_reports_dir()
    
    # 檢查並安裝依賴
    install_dependencies()
    
    # 生成各種報告
    behave_report = run_behave_report()
    pytest_report = run_pytest_report()
    coverage_report = run_coverage_report()
    
    # 清理舊報告
    cleanup_old_reports()
    
    # 總結
    print("\n📊 報告生成總結:")
    if behave_report:
        print(f"  ✅ Behave: {behave_report}")
    if pytest_report:
        print(f"  ✅ Pytest: {pytest_report}")
    if coverage_report:
        print(f"  ✅ Coverage: {coverage_report}")
    
    print("\n🎉 報告生成完成！")

if __name__ == "__main__":
    main() 