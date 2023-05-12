//dependencies {
//    implementation 'com.google.code.gson:gson:2.8.8'
//}

import com.google.gson.Gson
import com.google.gson.annotations.SerializedName

class MinhaClasse(@SerializedName("propriedade_1") val propriedade1: String, @SerializedName("propriedade_2") val propriedade2: Int) {
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