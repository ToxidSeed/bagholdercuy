export class ContratoOpcionBase {
    static MESES = {
        'JAN': 0, 'FEB': 1, 'MAR': 2, 'APR': 3, 'MAY': 4, 'JUN': 5,
        'JUL': 6, 'AUG': 7, 'SEP': 8, 'OCT': 9, 'NOV': 10, 'DEC': 11
    };

    static MESES_NOMBRES = Object.keys(ContratoOpcionBase.MESES);

    constructor() {
        this.imp_ejercicio = null;
        this.cod_tipo_opcion = null;
        this.fch_expiracion = null;
        this.cod_symbol_subyacente = null;
        this.value = null;
    }

    toHumanReadable() {
        if (!this.fch_expiracion) return null;

        const day = String(this.fch_expiracion.getDate()).padStart(2, '0');
        const month = ContratoOpcionBase.MESES_NOMBRES[this.fch_expiracion.getMonth()];
        const year = String(this.fch_expiracion.getFullYear()).slice(-2);

        let strike = this.imp_ejercicio.toString();

        return `${this.cod_symbol_subyacente} ${day}${month}${year} ${strike} ${this.cod_tipo_opcion}`;
    }

    toOCCExtendido() {
        if (!this.fch_expiracion) return null;

        const year = this.fch_expiracion.getFullYear();
        const month = String(this.fch_expiracion.getMonth() + 1).padStart(2, '0');
        const day = String(this.fch_expiracion.getDate()).padStart(2, '0');

        const fechaStr = `${year}${month}${day}`;

        const strikeInt = Math.round(this.imp_ejercicio * 1000);
        const strikeStr = String(strikeInt).padStart(8, '0');

        return `${this.cod_symbol_subyacente}${fechaStr}${this.cod_tipo_opcion}${strikeStr}`;
    }
}

export class ContratoOpcionHumanReadable extends ContratoOpcionBase {
    constructor(valor) {
        super();
        this.value = this._parse(valor);
    }

    _parse(valor) {
        if (!valor) return null;
        valor = valor.trim();

        const partes = valor.split(' ').filter(p => p !== '');
        if (partes.length !== 4) {
            throw new Error(`Formato inválido: '${valor}'. Se esperaba algo como 'SMCI 07FEB25 38 C'`);
        }
        this.cod_symbol_subyacente = partes[0].toUpperCase();
        this.fch_expiracion = this._parseFecha(partes[1]);
        this.imp_ejercicio = parseFloat(partes[2]);
        this.cod_tipo_opcion = partes[3].toUpperCase();

        if (this.cod_tipo_opcion !== 'P' && this.cod_tipo_opcion !== 'C') {
            throw new Error(`Tipo de opción inválido: '${this.cod_tipo_opcion}'. Se esperaba 'C' o 'P'`);
        }

        return valor;
    }

    _parseFecha(parte) {
        parte = parte.toUpperCase();
        if (parte.length !== 7) {
            throw new Error(`Formato de fecha inválido: '${parte}'. Se esperaba ddMMMYY`);
        }
        const dia = parseInt(parte.slice(0, 2), 10);
        const mesStr = parte.slice(2, 5);
        const anyo = 2000 + parseInt(parte.slice(5), 10);
        const mes = ContratoOpcionBase.MESES[mesStr];

        if (mes === undefined) {
            throw new Error(`Mes desconocido: '${mesStr}'`);
        }
        return new Date(anyo, mes, dia);
    }
}

export class ContratoOpcionExtendido extends ContratoOpcionBase {
    constructor(valor) {
        super();
        this.value = this._parse(valor);
    }

    _parse(valor) {
        if (!valor) return null;
        valor = valor.trim();

        this.imp_ejercicio = this._extraerEjercicio(valor);
        this.cod_tipo_opcion = this._extraerCodTipoOpcion(valor);
        this.fch_expiracion = this._extraerFchExpiracion(valor);
        this.cod_symbol_subyacente = this._extraerCodSymbolSubyacente(valor);

        return valor;
    }

    _extraerEjercicio(valor) {
        const strEjercicio = valor.slice(-8);
        return parseFloat(parseInt(strEjercicio, 10)) / 1000;
    }

    _extraerCodTipoOpcion(valor) {
        const codTipoOpcion = valor.slice(-9, -8);
        if (codTipoOpcion !== 'P' && codTipoOpcion !== 'C') {
            throw new Error(`No se encuentra el tipo de opcion en el codigo ${valor}, valor encontrado ${codTipoOpcion}`);
        }
        return codTipoOpcion;
    }

    _extraerFchExpiracion(valor) {
        const strFch = valor.slice(-17, -9);
        const year = parseInt(strFch.slice(0, 4), 10);
        const month = parseInt(strFch.slice(4, 6), 10) - 1; // 0-indexed in JS Date
        const day = parseInt(strFch.slice(6, 8), 10);
        return new Date(year, month, day);
    }

    _extraerCodSymbolSubyacente(valor) {
        return valor.slice(0, -17);
    }
}

// Factoría / Wrapper - Retorna la clase detectada manteniendo la compatibilidad
export class ContratoOpcion {
    constructor(valor) {
        if (!valor) return null;
        valor = valor.trim();

        if (valor.includes(' ')) {
            return new ContratoOpcionHumanReadable(valor);
        } else {
            return new ContratoOpcionExtendido(valor);
        }
    }
}
