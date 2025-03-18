import tensorflow as tf
from tensorflow import keras

# ✅ 커스텀 객체 등록 (mse 해결)
@keras.saving.register_keras_serializable()
class CustomMSE(keras.losses.MeanSquaredError):
    pass

# ✅ 모델 로드 (compile=False 설정 필수)
try:
    model = tf.keras.models.load_model("/app/model.h5", compile=False, custom_objects={"mse": CustomMSE()})
    print("✅ 모델 로드 성공!")
except Exception as e:
    print(f"❌ 모델 로드 실패: {e}")

# ✅ 샘플 예측 (테스트용)
import numpy as np
sample_input = np.array([[3.0]])  # 입력값 예시
prediction = model.predict(sample_input)
print(f"🎯 예측 결과: {prediction}")
