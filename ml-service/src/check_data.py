import pandas as pd
import os

print("="*60)
print("📊 TRAINING DATA STATISTICS")
print("="*60)

files = ['../data/spam.csv', '../data/emails.csv', '../data/spam_ham_dataset.csv']
total_rows = 0
datasets = []

for filepath in files:
    if os.path.exists(filepath):
        try:
            df = pd.read_csv(filepath, encoding='latin-1')
            rows = len(df)
            total_rows += rows
            datasets.append({
                'file': os.path.basename(filepath),
                'rows': rows
            })
            print(f"\n✅ {os.path.basename(filepath)}")
            print(f"   Total Rows: {rows:,}")
        except Exception as e:
            print(f"\n❌ {os.path.basename(filepath)}: Error - {e}")
    else:
        print(f"\n⚠️  {os.path.basename(filepath)}: Not found")

print("\n" + "="*60)
print(f"📈 TOTAL MESSAGES ACROSS ALL FILES: {total_rows:,}")
print("="*60)

# Now check after deduplication (like training does)
print("\n🔄 Checking after combining and deduplication...")

from train import SpamDetector
detector = SpamDetector()
df = detector.load_data('../data')

if df is not None:
    print(f"\n✨ ACTUAL TRAINING DATA (after deduplication):")
    print(f"   Total unique messages: {len(df):,}")
    print(f"   Spam messages: {(df['label']==1).sum():,}")
    print(f"   Ham messages: {(df['label']==0).sum():,}")
    print(f"   Spam percentage: {(df['label']==1).sum()/len(df)*100:.2f}%")
