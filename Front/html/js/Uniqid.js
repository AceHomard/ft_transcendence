class Uniqid {
    static _getRandom() {
        const randomNumber = Math.floor(Math.random() * 100);
        const formattedNumber = randomNumber.toString().padStart(2, '0');
        return formattedNumber;
    }

    static getUnixTimeStamp() {
        const nowUtc = new Date();
        const unixTimestamp = Math.floor(nowUtc.getTime() / 1000);
        return unixTimestamp;
    }

    static generate() {
        let uniqid = Uniqid._getRandom() + Uniqid._getRandom();
        uniqid += Uniqid.getUnixTimeStamp().toString();
        uniqid += Uniqid._getRandom() + Uniqid._getRandom();
        return uniqid;
    }
}

