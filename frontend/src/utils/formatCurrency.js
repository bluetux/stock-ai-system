export function formatCurrency(value, region = '미국', rate = null) {
    if (region === '한국') {
        return `${Number(value).toLocaleString()}원`;
    } else if (region === '미국') {
        const dollar = `$${Number(value).toLocaleString()}`;
        if (rate) {
            const won = (value * rate).toLocaleString();
            return `${dollar} (${won}원)`;
        }
        return dollar;
    }
    return value;
}
