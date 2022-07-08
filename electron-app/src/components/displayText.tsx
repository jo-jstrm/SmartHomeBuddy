export interface Props {
    text: string
}

export function displayText(props: Props) {
    return <p>{ props.text }</p>
}