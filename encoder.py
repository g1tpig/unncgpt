from sentence_transformers import SentenceTransformer

class Encoder:
    """
    这是一个简单的编码器类封装示例。
    """

    def __init__(self, encoding_type='utf-8'):
        """
        初始化编码器类。

        Parameters:
            encoding_type (str): 字符编码类型，默认为 'utf-8'。
        """
        self.encoding_type = encoding_type

    def encode(self, text):
        """
        对输入的文本进行编码。

        Parameters:
            text (str): 要编码的文本。

        Returns:
            bytes: 编码后的字节数据。
        """
        model = SentenceTransformer("distiluse-base-multilingual-cased-v1")
        encoded_data = model.encode(text, convert_to_numpy=True)
        return encoded_data

    def decode(self, encoded_data):
        """
        对编码后的字节数据进行解码。

        Parameters:
            encoded_data (bytes): 编码后的字节数据。

        Returns:
            str: 解码后的文本。
        """
        decoded_text = encoded_data.decode(self.encoding_type)
        return decoded_text

# 示例用法
if __name__ == "__main__":
    # 创建一个编码器实例
    encoder = Encoder()

    # 要编码的文本
    original_text = "Hello, World!"

    # 编码文本
    encoded_data = encoder.encode(original_text)
    print("Encoded Data:", encoded_data)

    # 解码数据
    decoded_text = encoder.decode(encoded_data)
    print("Decoded Text:", decoded_text)
