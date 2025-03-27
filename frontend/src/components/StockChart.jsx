import React, { useEffect, useRef, useState } from 'react';
import { createChart } from 'lightweight-charts';
import dayjs from 'dayjs';

const StockChart = ({ symbol, region, period = "1D" }) => {
    const priceChartRef = useRef(null);
    const volumeChartRef = useRef(null);
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // 캔들스틱/라인 차트 자동 결정
    const shouldUseCandlestick = ["5min", "1day", "1week", "1month"].includes(period);

    const fetchData = async (start = null, end = null) => {
        try {
            setLoading(true);
            let endpoint = `/api/stocks/${symbol}/history?period=${period}`;
            if (start && end) {
                endpoint += `&start=${start}&end=${end}`;
            }
            const response = await fetch(endpoint);
            if (!response.ok) throw new Error('데이터 로딩 실패');

            const rawData = await response.json();
            if (!Array.isArray(rawData) || rawData.length === 0) {
                setError('데이터가 없습니다');
                return;
            }

            const formattedData = rawData.map(item => {
                const timestamp = dayjs(item.timestamp);
                // 모든 기간에 대해 Unix timestamp 사용
                const time = timestamp.unix();

                if (!time || isNaN(time)) {
                    console.error('Invalid timestamp:', item.timestamp, timestamp);
                    return null;
                }

                return {
                    time,
                    open: Number(item.open || item.price || 0),
                    high: Number(item.high || item.price || 0),
                    low: Number(item.low || item.price || 0),
                    close: Number(item.close || item.price || 0),
                    value: Number(item.price || item.close || 0),
                    volume: Number(item.volume || 0),
                    MA5: item.MA5,
                    MA20: item.MA20,
                    predicted_price: item.predicted_price
                };
            }).filter(item => item !== null);

            if (formattedData.length === 0) {
                setError('유효한 데이터가 없습니다');
                return;
            }

            if (start && end) {
                setData(prevData => {
                    const newData = [...prevData, ...formattedData];
                    return newData
                        .sort((a, b) => a.time - b.time)
                        .filter((item, index, self) =>
                            index === 0 || item.time !== self[index - 1].time
                        );
                });
            } else {
                setData(formattedData);
            }
            setError(null);
        } catch (err) {
            console.error('Data fetch error:', err);
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
    }, [symbol, period]);

    useEffect(() => {
        if (!priceChartRef.current || !volumeChartRef.current || loading || error || !data.length) return;

        // 공통 차트 옵션
        const commonOptions = {
            layout: {
                background: { color: 'white' },
                textColor: 'black',
                fontSize: 11,
            },
            grid: {
                vertLines: { color: '#f0f3fa' },
                horzLines: { color: '#f0f3fa' },
            },
            handleScale: false,
            handleScroll: false,
            leftPriceScale: {
                visible: false,
            },
            rightPriceScale: {
                borderColor: '#f0f0f0',
                visible: true,
                autoScale: true,
                entireTextOnly: true,
                borderVisible: false,
                scaleMargins: {
                    top: 0.1,
                    bottom: 0.1,
                },
                width: 60,
            },
            timeScale: {
                borderColor: '#f0f0f0',
                rightOffset: 30,
                barSpacing: 6,
                fixLeftEdge: true,
                fixRightEdge: true,
                minBarSpacing: 6,
                rightBarStaysOnScroll: true,
                tickMarkFormatter: (time) => {
                    const date = dayjs.unix(time);
                    if (period === "5min") {
                        return date.format('HH:mm');
                    } else {
                        return date.format('MM/DD');
                    }
                },
            },
        };

        // 가격 차트 초기화
        const priceChart = createChart(priceChartRef.current, {
            ...commonOptions,
            width: priceChartRef.current.clientWidth + 24,  // 상단 차트는 24px 더 크게
            height: 400,
            timeScale: {
                ...commonOptions.timeScale,
                visible: false,
            },
        });

        // 거래량 차트 초기화
        const volumeChart = createChart(volumeChartRef.current, {
            ...commonOptions,
            width: priceChartRef.current.clientWidth,  // 기본 크기 사용
            height: 100,
            grid: {
                vertLines: { color: '#f0f3fa' },  // 그리드 다시 표시
                horzLines: { color: '#f0f3fa' },  // 그리드 다시 표시
            },
            timeScale: {
                ...commonOptions.timeScale,
                visible: true,
                timeVisible: true,
                secondsVisible: false,
            },
            rightPriceScale: {
                visible: false,
                borderVisible: false,
                width: 60,
            },
        });

        // 메인 시리즈 (캔들스틱 또는 라인)
        const mainSeries = shouldUseCandlestick
            ? priceChart.addCandlestickSeries({
                upColor: '#ff4d4f',
                downColor: '#1890ff',
                borderUpColor: '#ff4d4f',
                borderDownColor: '#1890ff',
                wickUpColor: '#ff4d4f',
                wickDownColor: '#1890ff',
                priceScaleId: 'right',  // 오른쪽 y축 사용
            })
            : priceChart.addAreaSeries({
                lineColor: '#1890ff',
                topColor: 'rgba(24, 144, 255, 0.4)',
                bottomColor: 'rgba(24, 144, 255, 0.0)',
                lineWidth: 2,
                priceScaleId: 'right',  // 오른쪽 y축 사용
            });

        // 거래량 시리즈
        const volumeSeries = volumeChart.addHistogramSeries({
            color: '#8884d8',
            priceFormat: {
                type: 'volume',
                formatter: () => ''  // 숫자를 빈 문자열로 반환
            },
            priceScaleId: 'volume',  // 독립적인 scale ID 사용
        });

        // 거래량 차트 y축 설정
        volumeChart.applyOptions({
            rightPriceScale: {
                visible: true,
                borderVisible: false,
                drawTicks: false,
                entireTextOnly: false,
                width: 60,
                scaleMargins: {
                    top: 0.1,
                    bottom: 0.1,
                },
                ticksVisible: false,
                mode: 2,  // Percentage 모드
                textColor: 'transparent',  // 텍스트 색상을 투명하게
            }
        });

        // MA 라인 시리즈
        let ma5Series, ma20Series, predictionSeries;
        if (data[0]?.MA5) {
            ma5Series = priceChart.addLineSeries({
                color: '#ffa116',
                lineWidth: 1,
                priceLineVisible: false,
                title: 'MA5',
                priceScaleId: 'right',  // 오른쪽 y축 사용
            });
        }
        if (data[0]?.MA20) {
            ma20Series = priceChart.addLineSeries({
                color: '#52c41a',
                lineWidth: 1,
                priceLineVisible: false,
                title: 'MA20',
                priceScaleId: 'right',  // 오른쪽 y축 사용
            });
        }
        if (data.some(d => d.predicted_price)) {
            predictionSeries = priceChart.addLineSeries({
                color: '#ff4d4f',
                lineWidth: 1,
                lineStyle: 2,
                priceLineVisible: false,
                title: 'AI 예측',
                priceScaleId: 'right',  // 오른쪽 y축 사용
            });
        }

        // 차트 여백 추가 설정
        const additionalOptions = {
            timeScale: {
                rightOffset: 12,  // 기본 여백으로 복원
                barSpacing: 6,
            },
        };

        const volumeOptions = {
            timeScale: {
                rightOffset: 30,  // 거래량 차트만 더 큰 여백
                barSpacing: 6,
            },
        };

        priceChart.applyOptions(additionalOptions);
        volumeChart.applyOptions(volumeOptions);

        try {
            // 데이터 적용
            mainSeries.setData(shouldUseCandlestick ? data : data.map(d => ({
                time: d.time,
                value: d.value
            })));

            volumeSeries.setData(data.map(d => ({
                time: d.time,
                value: d.volume,
                color: d.close >= d.open ? 'rgba(255, 77, 79, 0.5)' : 'rgba(24, 144, 255, 0.5)'
            })));

            if (ma5Series) {
                ma5Series.setData(data.filter(d => d.MA5).map(d => ({
                    time: d.time,
                    value: d.MA5
                })));
            }

            if (ma20Series) {
                ma20Series.setData(data.filter(d => d.MA20).map(d => ({
                    time: d.time,
                    value: d.MA20
                })));
            }

            if (predictionSeries) {
                predictionSeries.setData(data.filter(d => d.predicted_price).map(d => ({
                    time: d.time,
                    value: d.predicted_price
                })));
            }

            // 차트 범위 자동 조정
            priceChart.timeScale().fitContent();
            volumeChart.timeScale().fitContent();

            // 차트 동기화를 위한 공통 설정
            const syncCharts = () => {
                const mainScale = priceChart.timeScale();
                const volumeScale = volumeChart.timeScale();

                mainScale.subscribeVisibleTimeRangeChange(() => {
                    const visibleRange = mainScale.getVisibleRange();
                    if (visibleRange) {
                        volumeScale.setVisibleRange(visibleRange);
                    }
                });

                volumeScale.subscribeVisibleTimeRangeChange(() => {
                    const visibleRange = volumeScale.getVisibleRange();
                    if (visibleRange) {
                        mainScale.setVisibleRange(visibleRange);
                    }
                });
            };

            syncCharts();
        } catch (err) {
            console.error('Chart data error:', err);
        }

        // 차트 크기 조정 함수
        const resizeCharts = () => {
            if (!priceChartRef.current || !volumeChartRef.current) return;

            const containerWidth = priceChartRef.current.clientWidth;

            requestAnimationFrame(() => {
                priceChart.applyOptions({ width: containerWidth + 24 });  // 상단 차트는 24px 더 크게
                volumeChart.applyOptions({ width: containerWidth });  // 하단 차트는 기본 크기

                // 차트 범위 재조정
                priceChart.timeScale().fitContent();
                volumeChart.timeScale().fitContent();
            });
        };

        // 초기 크기 설정 및 리사이즈 이벤트 핸들러
        resizeCharts();
        const handleResize = () => {
            resizeCharts();
        };

        // ResizeObserver를 사용하여 컨테이너 크기 변화 감지
        const resizeObserver = new ResizeObserver(handleResize);
        resizeObserver.observe(priceChartRef.current);

        window.addEventListener('resize', handleResize);

        return () => {
            window.removeEventListener('resize', handleResize);
            resizeObserver.disconnect();
            priceChart.remove();
            volumeChart.remove();
        };
    }, [data, loading, error, symbol, period, shouldUseCandlestick]);

    if (loading) return <div className="h-full flex items-center justify-center">로딩중...</div>;
    if (error) return <div className="h-full flex items-center justify-center text-red-500">{error}</div>;
    if (!data || data.length === 0) return <div className="h-full flex items-center justify-center">데이터가 없습니다</div>;

    return (
        <div className="h-[550px] w-full pr-5">  {/* 오른쪽 패딩 추가 */}
            <div ref={priceChartRef} className="h-[400px] w-full" />
            <div ref={volumeChartRef} className="h-[100px] w-full" />
        </div>
    );
};

export default StockChart; 