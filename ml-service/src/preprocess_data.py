"""
Data Preprocessing Script
Combines and cleans all datasets in the data/ folder
Outputs a single master dataset ready for training
"""

import pandas as pd
import os
import re
from pathlib import Path

def clean_text(text):
    """Basic text cleaning"""
    if pd.isna(text):
        return ""
    # Convert to string
    text = str(text)
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)
    # Strip whitespace
    text = text.strip()
    return text

def load_spam_csv(file_path):
    """Load the original spam.csv (v1, v2 format)"""
    print(f"Loading {file_path}...")
    try:
        df = pd.read_csv(file_path, encoding='latin-1')
        # Take only first two columns
        df = df.iloc[:, :2]
        df.columns = ['label', 'text']
        # Normalize labels
        df['label'] = df['label'].str.lower()
        df['text'] = df['text'].apply(clean_text)
        # Remove empty texts
        df = df[df['text'].str.len() > 0]
        print(f"✓ Loaded {len(df)} messages from spam.csv")
        return df
    except Exception as e:
        print(f"✗ Error loading spam.csv: {e}")
        return pd.DataFrame(columns=['label', 'text'])

def load_emails_csv(file_path):
    """Load emails.csv (text, spam format)"""
    print(f"Loading {file_path}...")
    try:
        df = pd.read_csv(file_path)
        # Rename columns
        df.columns = ['text', 'spam']
        # Convert spam column (0/1) to ham/spam
        df['label'] = df['spam'].apply(lambda x: 'spam' if x == 1 else 'ham')
        df = df[['label', 'text']]
        df['text'] = df['text'].apply(clean_text)
        # Remove empty texts
        df = df[df['text'].str.len() > 0]
        print(f"✓ Loaded {len(df)} messages from emails.csv")
        return df
    except Exception as e:
        print(f"✗ Error loading emails.csv: {e}")
        return pd.DataFrame(columns=['label', 'text'])

def load_spam_ham_dataset(file_path):
    """Load spam_ham_dataset.csv (label, text, label_num format)"""
    print(f"Loading {file_path}...")
    try:
        df = pd.read_csv(file_path)
        # Take only label and text columns
        df = df[['label', 'text']]
        # Normalize labels
        df['label'] = df['label'].str.lower()
        df['text'] = df['text'].apply(clean_text)
        # Remove empty texts
        df = df[df['text'].str.len() > 0]
        print(f"✓ Loaded {len(df)} messages from spam_ham_dataset.csv")
        return df
    except Exception as e:
        print(f"✗ Error loading spam_ham_dataset.csv: {e}")
        return pd.DataFrame(columns=['label', 'text'])

def remove_duplicates(df):
    """Remove duplicate messages"""
    original_count = len(df)
    # Remove exact duplicates
    df = df.drop_duplicates(subset=['text'], keep='first')
    # Remove near-duplicates (same first 100 chars)
    df['text_start'] = df['text'].str[:100].str.lower()
    df = df.drop_duplicates(subset=['text_start'], keep='first')
    df = df.drop(columns=['text_start'])
    
    removed = original_count - len(df)
    print(f"✓ Removed {removed} duplicate messages")
    return df

def balance_dataset(df, max_ratio=2.0):
    """Balance ham/spam ratio (optional)"""
    spam_count = len(df[df['label'] == 'spam'])
    ham_count = len(df[df['label'] == 'ham'])
    
    print(f"\nOriginal distribution:")
    print(f"  Spam: {spam_count:,} ({spam_count/len(df)*100:.1f}%)")
    print(f"  Ham: {ham_count:,} ({ham_count/len(df)*100:.1f}%)")
    
    ratio = max(spam_count, ham_count) / min(spam_count, ham_count)
    
    if ratio > max_ratio:
        print(f"⚠ Imbalanced dataset (ratio: {ratio:.2f}:1)")
        # Downsample majority class
        if spam_count > ham_count:
            spam_df = df[df['label'] == 'spam'].sample(n=int(ham_count * max_ratio), random_state=42)
            ham_df = df[df['label'] == 'ham']
        else:
            ham_df = df[df['label'] == 'ham'].sample(n=int(spam_count * max_ratio), random_state=42)
            spam_df = df[df['label'] == 'spam']
        
        df = pd.concat([spam_df, ham_df], ignore_index=True)
        print(f"✓ Balanced to max ratio {max_ratio}:1")
    else:
        print(f"✓ Dataset is reasonably balanced (ratio: {ratio:.2f}:1)")
    
    return df

def preprocess_all_datasets():
    """Main preprocessing function"""
    print("=" * 60)
    print("🔄 DATA PREPROCESSING STARTED")
    print("=" * 60)
    
    # Get paths
    script_dir = Path(__file__).parent
    data_dir = script_dir.parent / 'data'
    
    # Load all datasets
    datasets = []
    
    spam_csv_path = data_dir / 'spam.csv'
    if spam_csv_path.exists():
        datasets.append(load_spam_csv(spam_csv_path))
    
    emails_csv_path = data_dir / 'emails.csv'
    if emails_csv_path.exists():
        datasets.append(load_emails_csv(emails_csv_path))
    
    spam_ham_path = data_dir / 'spam_ham_dataset.csv'
    if spam_ham_path.exists():
        datasets.append(load_spam_ham_dataset(spam_ham_path))
    
    if not datasets:
        print("✗ No datasets found!")
        return
    
    # Combine all datasets
    print(f"\n{'='*60}")
    print("📦 COMBINING DATASETS")
    print("=" * 60)
    combined_df = pd.concat(datasets, ignore_index=True)
    print(f"✓ Combined total: {len(combined_df):,} messages")
    
    # Remove duplicates
    print(f"\n{'='*60}")
    print("🧹 CLEANING DATA")
    print("=" * 60)
    combined_df = remove_duplicates(combined_df)
    
    # Shuffle
    combined_df = combined_df.sample(frac=1, random_state=42).reset_index(drop=True)
    print("✓ Shuffled dataset")
    
    # Balance dataset
    print(f"\n{'='*60}")
    print("⚖️  BALANCING DATASET")
    print("=" * 60)
    combined_df = balance_dataset(combined_df, max_ratio=2.0)
    
    # Save master dataset
    output_path = data_dir / 'master_dataset.csv'
    combined_df.to_csv(output_path, index=False, encoding='utf-8')
    
    print(f"\n{'='*60}")
    print("✅ PREPROCESSING COMPLETE")
    print("=" * 60)
    print(f"📁 Output file: {output_path}")
    print(f"📊 Total messages: {len(combined_df):,}")
    
    spam_count = len(combined_df[combined_df['label'] == 'spam'])
    ham_count = len(combined_df[combined_df['label'] == 'ham'])
    print(f"📧 Spam messages: {spam_count:,} ({spam_count/len(combined_df)*100:.1f}%)")
    print(f"📬 Ham messages: {ham_count:,} ({ham_count/len(combined_df)*100:.1f}%)")
    
    # Show sample
    print(f"\n{'='*60}")
    print("📝 SAMPLE DATA")
    print("=" * 60)
    print(combined_df.head(10).to_string(index=False))
    
    return combined_df

if __name__ == "__main__":
    preprocess_all_datasets()
