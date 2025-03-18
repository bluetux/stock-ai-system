import tensorflow as tf
from tensorflow import keras
import numpy as np

# ✅ 명시적인 loss 함수 사용
mse_loss = keras.losses.MeanSquaredError()

# ✅ 간단한 모델 생성
model = keras.Sequential([
    keras.layers.Input(shape=(1,)),  # ✅ batch_shape 대신 Input 사용
    keras.layers.Dense(10, activation="relu"),
    keras.layers.Dense(1)
])

model.compile(optimizer="adam", loss=mse_loss)  # ✅ mse 대신 명시적인 loss 함수 사용

# ✅ 학습 데이터
x_train = np.array([1, 2, 3, 4, 5], dtype=np.float32)
y_train = np.array([2, 4, 6, 8, 10], dtype=np.float32)

# ✅ 모델 학습
model.fit(x_train, y_train, epochs=10, verbose=0)

# ✅ 모델 저장
model.save("model.h5", save_format='h5')
print("✅ model.h5 저장 완료!")
