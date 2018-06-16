-- example HTTP POST script which demonstrates setting the
-- HTTP method, body, and adding a header

wrk.method = "POST"
wrk.body   = '--bced8a6a76a2411b9da4f7ad5dbedf4f\r\nContent-Disposition: form-data; name="a"\r\n\r\n1\r\n--bced8a6a76a2411b9da4f7ad5dbedf4f\r\nContent-Disposition: form-data; name="b"\r\n\r\n2\r\n--bced8a6a76a2411b9da4f7ad5dbedf4f\r\nContent-Disposition: form-data; name="c"\r\n\r\n3\r\n--bced8a6a76a2411b9da4f7ad5dbedf4f\r\nContent-Disposition: form-data; name="d"\r\n\r\n4\r\n--bced8a6a76a2411b9da4f7ad5dbedf4f\r\nContent-Disposition: form-data; name="e"\r\n\r\n5\r\n--bced8a6a76a2411b9da4f7ad5dbedf4f\r\nContent-Disposition: form-data; name="test"; filename="download"\r\n\r\nhello world\r\n--bced8a6a76a2411b9da4f7ad5dbedf4f--\r\n'
wrk.headers["Content-Type"] = "multipart/form-data; boundary=bced8a6a76a2411b9da4f7ad5dbedf4f"