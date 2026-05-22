import SwiftUI

struct BotFaceView: View {

    var body: some View {
        Image("face")
            .resizable()
            .aspectRatio(contentMode: .fit)
            .clipped()
    }
}

#Preview {
    BotFaceView()
        .frame(width: 200)
        .padding()
        .background(Color.white)
}
