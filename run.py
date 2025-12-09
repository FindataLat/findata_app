from findata import findata_main

if __name__ == "__main__":
    app = findata_main()
    app.run(host="0.0.0.0", port=443, debug=True)