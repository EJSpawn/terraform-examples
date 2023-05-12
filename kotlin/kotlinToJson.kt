//dependencies {
//    implementation 'com.google.code.gson:gson:2.8.8'
//}

import com.google.gson.Gson

class MinhaClasse(val propriedade1: String, val propriedade2: Int) {
    fun toJson(): String {
        val gson = Gson()
        return gson.toJson(this)
    }
}

fun main() {
    val minhaClasse = MinhaClasse("Hello", 123)
    val json = minhaClasse.toJson()
    println(json)
}