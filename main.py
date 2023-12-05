# main.py
import streamlit as st

from app.flows.data4finetuning.main import data4finetuning

def main():
    data4finetuning()

if __name__ == "__main__":
    main()
