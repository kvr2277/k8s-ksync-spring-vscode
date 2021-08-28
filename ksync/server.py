return jsonify({
    "ksync": True,
    "restart": LAST_RESTART,
    "pod": os.environ.get('POD_NAME'),
    "files": file_list,
})