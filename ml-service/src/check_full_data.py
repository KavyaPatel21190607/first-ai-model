import pandas as pd
import os

print("="*60)
print("🔍 CHECKING FULL DATASET SIZE")
print("="*60)

filepath = '../data/spam_ham_dataset.csv'

try:
    df = pd.read_csv(filepath, encoding='latin-1')
    print(f"\n✅ spam_ham_dataset.csv")
    print(f"   Total rows: {len(df):,}")
    print(f"   Columns: {list(df.columns)}")
    
    if 'label' in df.columns:
        print(f"\n📊 Label Distribution:")
        print(df['label'].value_counts())
        print(f"\n   Spam: {(df['label']=='spam').sum():,}")
        print(f"   Ham: {(df['label']=='ham').sum():,}")
    
    print(f"\n🔍 First 3 rows:")
    print(df.head(3))
    
    print(f"\n⚠️  IMPORTANT:")
    print(f"   Full file has {len(df):,} rows")
    print(f"   But training only loaded 5,171 rows")
    print(f"   You're using only 5% of available data!")
    
except Exception as e:
    print(f"❌ Error: {e}")
